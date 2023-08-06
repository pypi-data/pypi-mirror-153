#!/usr/bin/env python
# coding=utf-8

import os
from xml.dom.minidom import Document
from xml.dom.minidom import parse as parse
import xml.dom.minidom


class NoseXML(object):

    def __init__(self):

        impl = xml.dom.minidom.getDOMImplementation()
        self.dom = impl.createDocument(None, 'testsuite', None)
        self.root = self.dom.documentElement
        self._test = 0
        self._fail = 0
        self._pass = 0

    def _get_test_count(self, verdict):
        self._test = len(verdict)
        self._pass = len(filter(lambda n: n['test_result'] == Verdict.PASSED, verdict))
        self._fail = len(filter(lambda n: n['test_result'] == Verdict.FAILED, verdict))

    def _set_root_attr(self):
        self.root.setAttribute('name', 'nosetests')
        self.root.setAttribute('tests', str(self._test))
        self.root.setAttribute('failures', str(self._fail))
        self.root.setAttribute('pass', str(self._pass))

    def generate_xml(self, verdict):

        self._get_test_count(verdict)
        self._set_root_attr()
        for item in verdict:
            self._create_testcase_element(self.root, item)
        self.create_xml_file('nosetests.xml')

    def _create_testcase_element(self, parent_element, verdict):
        element = self.dom.createElement('testcase')
        element.setAttribute('classname', verdict['test_name'])
        element.setAttribute('name', verdict['test_name'])
        parent_element.appendChild(element)

        if verdict['test_result'] is not Verdict.PASSED:
            fail_element = self._create_failure_element(verdict)
            element.appendChild(fail_element)
        sys_out = self.dom.createElement('system-out')
        date = self.dom.createCDATASection(verdict['comment'])
        sys_out.appendChild(date)
        element.appendChild(sys_out)

    def _create_failure_element(self, verdict):
        fail_element = self.dom.createElement('failure')
        fail_element.setAttribute('type', 'exceptions. Error')
        fail_element.setAttribute('message', 'message: test case Error')
        date = self.dom.createCDATASection(verdict['comment'])
        fail_element.appendChild(date)
        return fail_element

    def create_xml_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.dom.toprettyxml(indent='\t', encoding='utf-8'))

    def parse_xml(self, xml_file):
        if xml_file is not None and os.path.exists(xml_file):
            DOMTree = parse(xml_file)
            Data = DOMTree.documentElement
            fail_out = self._get_failure_messge(Data)
            error_out = self._get_error_messge(Data)
            out_put = fail_out + error_out
            out_put = out_put.replace('\\n', '\n')
        else:
            out_put = ''
        return out_put

    def _get_failure_messge(self, root):
        nodes = root.getElementsByTagName('failure')
        out_put = ''
        for node in nodes:
            data = node.childNodes[0].data
            out_put = out_put + data
        return out_put

    def _get_error_messge(self, root):
        nodes = root.getElementsByTagName('error')
        out_put = ''
        for node in nodes:
            data = node.childNodes[0].data
            out_put = out_put + data
        return out_put


A = NoseXML()
B = A.parse_xml(r"D:\Automaiton\new_production\productionautomation\log\nosetests_test_rand_mix_rw_70_30_1583823250.6500623.xml")
print(B)