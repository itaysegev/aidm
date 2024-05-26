from pddlgymnasium.parser import PDDLDomainParser, PDDLProblemParser
from pddlgymnasium.spaces import LiteralSpace
from pddlgymnasium.structs import Predicate, Literal, Type, Not, Anti, LiteralConjunction, State

from aidm.environments.pddl.pddl_problem import PDDLProblem
from aidm.rl.q_learning import q_learning
from aidm.core.utils import CriteriaGoalState, print_results
from aidm.search.heuristic import goal_heuristic, zero_heuristic
from pddl import DOMAIN,PROBLEM

def test_pddl_rl():

    # create a wrapper of the environment to the search
    problem = PDDLProblem(domain='domain.pddl', problem='problem0.2.pddl')

    # perform q_learning
    [best_node, best_plan, resources] = q_learning(problem=problem)

    print_results(info='q-learning', node=best_node, plan=best_plan, resources=resources)

if __name__ == "__main__":
    test_pddl_rl()
