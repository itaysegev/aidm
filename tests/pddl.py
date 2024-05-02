DOMAIN = """
(define (domain n-table-blocks-world)
  (:requirements :strips :typing :equality)
  (:types block color table)
  (:predicates (on ?b1 ?b2 - block)
	           (ontable ?b - block ?t -table)
	           (clear ?b - block)
	           (handempty)
	           (holding ?b - block)
	           (bcolor ?b - block ?c -color)
 )

  (:action pick-up
	     :parameters (?b - block ?t - table)
	     :precondition (and (clear ?b)(ontable ?b ?t)(handempty))
	     :effect
	     (and (not (ontable ?b ?t))
		   (not (clear ?b))
		   (not (handempty))
		   (holding ?b)))

  (:action put-down
	     :parameters (?b - block ?t - table)
	     :precondition (holding ?b)
	     :effect
	     (and (not (holding ?b))
		   (clear ?b)
		   (handempty)
		   (ontable ?b ?t)))

  (:action stack
	     :parameters (?b1 ?b2 - block)
	     :precondition (and (holding ?b1) (clear ?b2))
	     :effect
	     (and (not (holding ?b1))
		   (not (clear ?b2))
		   (clear ?b1)
		   (handempty)
		   (on ?b1 ?b2)))

  (:action unstack
	     :parameters (?b1 ?b2 - block)
	     :precondition (and (on ?b1 ?b2) (clear ?b1)(handempty))
	     :effect
	     (and (holding ?b1)
		   (clear ?b2)
		   (not (clear ?b1))
		   (not (handempty))
		   (not (on ?b1 ?b2)))))

"""

PROBLEM2 = """
(define (problem 3t5b)
(:domain n-table-blocks-world)
(:objects 
B1 B2 B3 B4 B5 - block
Y B G R P - color
T1 T2 T3  - table
)
(:init
(handempty)

(ontable B1 T1)
(clear B1)
(bcolor B1 Y)

(ontable B2 T1)
(clear B2)
(bcolor B2 B)

(ontable B3 T2)
(clear B3)
(bcolor B3 Y)

(ontable B4 T3)
(clear B4)
(bcolor B4 G)

(ontable B5 T3)
(clear B5)
(bcolor B5 R)

)
(:goal (and
(ontable B1 T3)
(ontable B2 T2)
))
)
"""

PROBLEM2 = """
(define (problem 3t5b)
(:domain n-table-blocks-world)
(:objects 
B1 B2 - block
Y B - color
T1 - table
)
(:init
(handempty)

(ontable B1 T1)
(clear B1)
(bcolor B1 Y)

(ontable B2 T1)
(clear B2)
(bcolor B2 B)

)
(:goal (and
(holding B2)
))
)
"""




PROBLEM = """
(define (problem 3t5b)
(:domain n-table-blocks-world)
(:objects 
B1 B2 - block
Y B - color
T1 T2 - table
)
(:init
(handempty)

(ontable B1 T1)
(clear B1)
(bcolor B1 Y)

(ontable B2 T1)
(clear B2)
(bcolor B2 B)

)
(:goal (and
(ontable B2 T2)
))
)
"""