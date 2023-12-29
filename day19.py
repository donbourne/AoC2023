import re


class Comparator:
    def __init__(self, subject, comparator, value):
        self.subject = subject
        self.comparator = comparator
        self.value = value

    def __str__(self):
        return f'comparator: {self.subject} {self.comparator} {self.value}'

    def __repr__(self):
        return self.__str__()

    def matches(self, part):
        if self.comparator == '>':
            return part.get(self.subject) > self.value
        elif self.comparator == '<':
            return part.get(self.subject) < self.value

    def get_reverse(self):
        reversed_comparator = '>=' if self.comparator == '<' else '<='
        return Comparator(self.subject, reversed_comparator, self.value)


class Part:

    def __init__(self, x, m, a, s):
        self.values = {}
        self.values['x'] = x
        self.values['m'] = m
        self.values['a'] = a
        self.values['s'] = s

    def __str__(self):
        return f"[x: {self.values['x']} m: {self.values['m']}, a: {self.values['a']}, s: {self.values['s']}]"

    def __repr__(self):
        return self.__str__()

    def total(self):
        return self.values['x'] + self.values['m'] + self.values['a'] + self.values['s']

    def get(self, s):
        return self.values[s]


workflow_strs = []
part_strs = []
workflow_lines = True
with open('day19.txt', 'rt') as f:
    lines = [line.strip() for line in f.readlines()]

for line in lines:
    if line == '':
        workflow_lines = False
    else:
        if workflow_lines:
            workflow_strs.append(line)
        else:
            part_strs.append(line)


# create mapping from workflow name to list of conditions
workflow_rules = {}
for workflow in workflow_strs:
    name, condition_actions = workflow.split('{')
    condition_actions = condition_actions.replace('}', '')
    # print(condition_actions)
    condition_actions = condition_actions.split(",")
    # print(condition_actions)
    rules = []
    for condition_action in condition_actions:

        if ':' in condition_action:
            condition, next_workflow = condition_action.split(':')
            # print(condition, next_workflow)
            match = re.search(r'([xmas])([<>])(\d+)', condition)
            comparator = Comparator(match.group(1), match.group(2), int(match.group(3)))
            rules.append((comparator, next_workflow))
        else:
            next_workflow = condition_action
            rules.append((None, next_workflow))
    workflow_rules[name] = rules


parts = []
for part in part_strs:
    part = part.replace("{", '').replace("}", '')
    ratings = part.split(',')
    ratings = [int(rating[2:]) for rating in ratings]
    part = Part(*ratings)
    parts.append(part)

# add the ratings from the accepted parts together
accepted_parts = []
for part in parts:
    rules = workflow_rules['in']
    done = False
    rule_index = 0
    while not done:
        comparator, next_workflow = rules[rule_index]
        rule_index += 1
        if not comparator or comparator.matches(part):
            if next_workflow == 'A':
                accepted_parts.append(part)
                done = True
            elif next_workflow == 'R':
                done = True
            else:
                rule_index = 0
                rules = workflow_rules[next_workflow]

total = 0
for accepted_part in accepted_parts:
    total += accepted_part.total()
print(total)

# part 2
'''
create an empty list of comparator lists
for each workflow
    create a list of (workflow name, comparator list) that lead to that workflow
for each (workflow name w, comparator list comp_original) that leads to A
    start new list comps of comparators = comp_original copy
    for each (workflow name, comparator list comp_new) that leads to w
        if comp_new doesn't conflict with comp_original
            add comp_new to comps
     
# create list of workflows that lead to each 
# find all the workflows that lead to A
# create set of rules for getting to the A destination in that workflow
'''

class RangeTracker():

    def __init__(self, workflow_antecedent_chain):
        self.mins = {'x': 1, 'm': 1, 'a': 1, 's': 1}
        self.maxs = {'x': 4000, 'm': 4000, 'a': 4000, 's': 4000}
        for _, comparators in workflow_antecedent_chain:
            for comparator in comparators:
                match comparator.comparator:
                    case '<':
                        self.maxs[comparator.subject] = min(comparator.value - 1, self.maxs[comparator.subject])
                    case '<=':
                        self.maxs[comparator.subject] = min(comparator.value, self.maxs[comparator.subject])
                    case '>':
                        self.mins[comparator.subject] = max(comparator.value + 1, self.mins[comparator.subject])
                    case '>=':
                        self.mins[comparator.subject] = max(comparator.value, self.mins[comparator.subject])

    def combo_count(self):
        counts = [self.maxs[letter] - self.mins[letter] + 1 for letter in ('x', 'm', 'a', 's')]
        product = 1
        for count in counts:
            product *= count
        return product

    def __repr__(self):
        s = ''
        for letter in ('x', 'm', 'a', 's'):
            s += f'{letter}: {self.mins[letter]} - {self.maxs[letter]}\n'
        return s

'''
build a map showing how to get to each workflow
to_name: (from_name, [comparator, comparator, comparator])
'''
workflow_antecedents = {}
workflow_antecedents['A'] = []
workflow_antecedents['R'] = []
for workflow_name in workflow_rules:
    workflow_antecedents[workflow_name] = []

for from_name, rules in workflow_rules.items():
    # print(from_name, rules)
    for i in range(len(rules)):
        rule_subset = rules[0:i+1]
        to_name = rule_subset[-1][1]
        comparators = []
        for rule in rule_subset[0:-1]:
            if rule[0]:
                comparators.append(rule[0].get_reverse())
        if rule_subset[-1][0]:
            comparators.append(rule_subset[-1][0])

        workflow_antecedents[to_name].append((from_name, comparators))
    #     print(from_name, comparators, '->', to_name)
    # print()

# now combine workflow antecedents that start from 'in' and end at 'A' by prepending workflow antecedents
workflow_antecedent_chains = []
target = 'A'
for workflow_antecedent in workflow_antecedents[target]:
    workflow_antecedent_chain = []
    workflow_antecedent_chain.append((workflow_antecedent[0], workflow_antecedent[1]))   # YOU ARE HERE
    from_name = workflow_antecedent[0]
    while from_name != 'in':
        # relying here on the fact that only A and R have more than one antecedent
        workflow_antecedent_chain.insert(0, *workflow_antecedents[from_name])
        from_name = workflow_antecedents[from_name][0][0]
    workflow_antecedent_chains.append(workflow_antecedent_chain)
    # print(workflow_antecedent_chain)

total = 0
for workflow_antecedent_chain in workflow_antecedent_chains:
    range_tracker = RangeTracker(workflow_antecedent_chain)
    total += range_tracker.combo_count()
    # print(range_tracker)

print(total)
