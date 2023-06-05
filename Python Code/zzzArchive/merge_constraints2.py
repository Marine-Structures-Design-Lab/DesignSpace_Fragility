# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:44:03 2023

@author: joeyv
"""
import sympy as sp

# Method 1

def remove_redundancies2(rules):
    simplified_rules = []
    for rule in rules:
        if not is_redundant(rule, simplified_rules):
            simplified_rules.append(rule)
    return simplified_rules

def is_redundant(rule, rules):
    if isinstance(rule, sp.Or):
        for condition in rule.args:
            var = condition.lhs
            if condition.rel_op == '<=':
                for other_rule in rules:
                    if isinstance(other_rule, sp.Or):
                        for other_condition in other_rule.args:
                            if other_condition.lhs == var and other_condition.rhs > condition.rhs:
                                return True
            elif condition.rel_op == '>':
                for other_rule in rules:
                    if isinstance(other_rule, sp.Or):
                        for other_condition in other_rule.args:
                            if other_condition.lhs == var and other_condition.rhs < condition.rhs:
                                return True
    else:
        var = rule.lhs
        if rule.rel_op == '<=':
            for other_rule in rules:
                if isinstance(other_rule, sp.Or):
                    for other_condition in other_rule.args:
                        if other_condition.lhs == var and other_condition.rhs > rule.rhs:
                            return True
        elif rule.rel_op == '>':
            for other_rule in rules:
                if isinstance(other_rule, sp.Or):
                    for other_condition in other_rule.args:
                        if other_condition.lhs == var and other_condition.rhs < rule.rhs:
                            return True
    return False