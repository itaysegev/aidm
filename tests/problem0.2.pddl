(define (problem 3t5b)
(:domain n-table-blocks-world)
(:objects 
B1 B2 B3 - block
Y B G  - color
T1 T2   - table
)
(:init
(handempty)

(on B1 B2)
(clear B1)
(bcolor B1 Y)

(ontable B2 T1)
(bcolor B2 B)

(ontable B3 T2)
(clear B3)
(bcolor B3 Y)

)
(:goal (and
(on B2 B3)
))
)