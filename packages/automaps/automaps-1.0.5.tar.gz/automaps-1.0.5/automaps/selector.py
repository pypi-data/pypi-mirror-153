from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

import pandas as pd
import streamlit as st

import automaps.db


class BaseSelector(ABC):
    label: str
    options: Optional[Iterable[Any]]
    widget_method: Optional[Callable]
    no_value_selected_text: Optional[str]
    widget_args: Optional[Dict[str, Any]]
    depends_on_selectors: Union[List[str], Dict[str, Any]]
    provide_raw_options: bool = False
    options_raw: Iterable[Any]
    label_ui: Optional[str]
    optional: bool
    exclude_from_filename: bool
    use_for_file_format: bool
    debug: bool  # TODO: documentation & tests

    @abstractmethod
    def widget(self):
        pass


class SelectorSimple(BaseSelector):
    def __init__(
        self,
        label: str,
        options: Iterable[Any],
        widget_method: Optional[Callable] = None,
        widget_args: dict = {},
        no_value_selected_text: str = "",
        depends_on_selectors: Union[List[str], Dict[str, Any]] = {},
        label_ui: Optional[str] = None,
        optional: bool = False,
        exclude_from_filename: bool = False,
        use_for_file_format: bool = False,
        debug: bool = False,
    ):
        self.label = label
        self.options = list(options)
        self.no_value_selected_text = no_value_selected_text
        if len(no_value_selected_text) > 0:
            self.options = [no_value_selected_text] + self.options
        self.widget_method = widget_method
        self.widget_args = widget_args
        self.depends_on_selectors = depends_on_selectors
        self.label_ui = label_ui
        self.optional = optional
        self.exclude_from_filename = exclude_from_filename
        self.use_for_file_format = use_for_file_format
        self.debug = debug  # TODO: documentation & tests

    @property
    def widget(self):
        if self.widget_method:
            return self.widget_method(
                self.label_ui if self.label_ui else self.label,
                self.options,
                **self.widget_args
            )
        else:
            if len(self.options) == 0:
                return None
            else:
                return self.options


class SelectorSQL(BaseSelector):
    def __init__(
        self,
        label: str,
        sql: str,
        widget_method: Optional[Callable] = None,
        widget_args: dict = {},
        no_value_selected_text: str = "",
        additional_values: Iterable[Any] = [],
        depends_on_selectors: Union[List[str], Dict[str, Any]] = {},
        provide_raw_options: bool = False,
        label_ui: Optional[str] = None,
        optional: bool = False,
        exclude_from_filename: bool = False,
        extract_first_option: bool = False,
        retrieve_as_dictionary: bool = False,  # TODO: documentation & tests
        use_for_file_format: bool = False,
        debug: bool = False,  # TODO: documentation & tests
    ):
        self.label = label
        self.sql = sql
        self.sql_orig = sql
        self.widget_method = widget_method
        self.no_value_selected_text: str = no_value_selected_text
        self.additional_values = list(additional_values)
        self.widget_args = widget_args
        self.depends_on_selectors = depends_on_selectors
        self.provide_raw_options = provide_raw_options
        self.label_ui = label_ui
        self.optional = optional
        self.exclude_from_filename = exclude_from_filename
        self.extract_first_option = extract_first_option
        self.retrieve_as_dictionary = retrieve_as_dictionary
        self.use_for_file_format = use_for_file_format
        self.debug = debug

    @property
    def options(self) -> Iterable[Any]:  # type: ignore
        options = read_options_sql(self.sql, self.retrieve_as_dictionary)
        self.options_raw = options
        if (len(self.additional_values) > 0) and (len(options) > 0):
            options = list(self.additional_values) + options
        if len(self.no_value_selected_text) > 0:
            options = [self.no_value_selected_text] + options
        return options

    @property
    def widget(self):
        if self.widget_method:
            return self.widget_method(
                self.label_ui if self.label_ui else self.label,
                self.options,
                **self.widget_args
            )
        else:
            if len(self.options) == 0:
                return None
            elif self.extract_first_option:
                return self.options[0]
            else:
                return self.options


@st.cache(show_spinner=False)
def read_options_sql(sql, as_dict=False) -> Iterable[Any]:
    if as_dict:
        return pd.read_sql(sql, automaps.db.get_engine()).to_dict(orient="records")
    return list(pd.read_sql(sql, automaps.db.get_engine()).iloc[:, 0])


class MultiSelector:
    def __init__(
        self,
        label: str,
        selectors: List[BaseSelector],
        exclude_from_filename: bool = False,
        use_for_file_format: bool = False,
    ):
        self.label = label
        self.selectors = selectors
        self.exclude_from_filename = exclude_from_filename
        self.use_for_file_format = use_for_file_format
