#!/usr/bin/env python

"""This is the test module for XesXmlParser.

This module tests the XesXmlParser.
"""


import pytest, os, tempfile
from opyenxes.data_in.XesXmlParser import XesXmlParser
from opyenxes.out.XesXmlSerializer import XesXmlSerializer
from opyenxes.factory.XFactory import XFactory


__author__ = "Wai Lam Jonathan Lee"
__email__ = "walee@uc.cl"


@pytest.fixture()
def cleandir():
    # make empty directory to conduct tests
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)


@pytest.fixture(scope='module')
def log():
    log = XFactory.create_log()
    # add some log features
    log.set_features('f1', 0)
    # add some log attributes
    str_attr = XFactory.create_attribute_literal('l_attr', 'UNKNOWN')
    log.get_attributes()['l_attr'] = str_attr
    # add a trace
    tracelen = 2
    trace0 = XFactory.create_trace()
    # add some trace attributes
    bool_attr = XFactory.create_attribute_boolean('t_attr', True)
    trace0.get_attributes()['t_attr'] = bool_attr
    for i in range(tracelen):
        event = XFactory.create_event()
        # add an attribute
        int_attr = XFactory.create_attribute_discrete('e_attr', 0)
        event.get_attributes()['e_attr0'] = int_attr
        trace0.append(event)
    log.append(trace0)
    return log


def export_log(log, fpath):
    with open(fpath, 'w') as f:
        XesXmlSerializer().serialize(log, f)


# clean directory fixture is ran before every test method
@pytest.mark.usefixtures('cleandir')
class TestXesXmlParser:
    @pytest.fixture(autouse=True)
    def setup(self, log):
        self.log = log
        self.parser = XesXmlParser()

    def read_log(self, fpath):
        with open(fpath, 'r') as log_file:
            log = self.parser.parse(log_file)[0]
        return log

    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []

    def test_cwd_starts_with_log(self):
        export_log(self.log, 'log.xes')
        assert os.listdir(os.getcwd()) == ['log.xes']

    def test_can_parse_log(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        assert log is not None

    def test_parsed_log_has_feature(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        log_features = log.get_features()
        assert 'f1' in log_features
        assert log_features['f1'] == 0

    def test_parsed_log_has_attributes(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        log_attrs = log.get_attributes()
        assert 'l_attr' in log_attrs
        attr0 = log_attrs['l_attr']
        assert attr0.get_value() == 'UNKNOWN'

    def test_parsed_log_has_proper_trace_and_events(self):
        export_log(self.log, 'log.xes')
        log = self.read_log('log.xes')
        assert len(log) == 1
        trace = log[0]
        trace_attrs = trace.get_attributes()
        assert 't_attr' in trace_attrs
        t_attr = trace_attrs['t_attr']
        assert t_attr.get_value() == True
        assert len(trace) == 2
        e0 = trace[0]
        event_attrs_0 = e0.get_attributes()
        assert 'e_attr' in event_attrs_0
        e_attr_0 = event_attrs_0['e_attr']
        assert e_attr_0.get_value() == 0
        e1 = trace[1]
        event_attrs_1 = e1.get_attributes()
        assert 'e_attr' in event_attrs_1
        e_attr_1 = event_attrs_1['e_attr']
        assert e_attr_1.get_value() == 0
