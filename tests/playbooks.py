#! /usr/bin/env python3

# Test that key parts of Playbooks stayed in the right places

import unittest
import framework

class TestPlaybooks(framework.TestPlaybooks):
    
    def test_cabalist(self):
        playbook = self.playbook_test("cabalist", "The Cabalist", True)
        self.assert_box(playbook[0], 0, "Paradigm List", "MIDDLE", "contains")

    def test_hedge_mage(self):
        playbook = self.playbook_test("hedge_mage", "The Hedge Mage")

    def test_inspired(self):
        playbook = self.playbook_test("inspired", "The Inspired")

    def test_mentor(self):
        playbook = self.playbook_test("mentor", "The Mentor", True)
        self.assert_box(playbook[0], 0, "Paradigm List", "MIDDLE", "contains")

    def test_pious(self):
        playbook = self.playbook_test("pious", "The Pious")

    def test_primordial(self):
        playbook = self.playbook_test("primordial", "The Primordial")

    def test_tech_adept(self):
        playbook = self.playbook_test("tech_adept", "The Tech Adept")

    def test_voiced(self):
        playbook = self.playbook_test("voiced", "The Voiced")

    def test_wayfarer(self):
        playbook = self.playbook_test("wayfarer", "The Wayfarer")


if __name__ == "__main__":
    unittest.main()
