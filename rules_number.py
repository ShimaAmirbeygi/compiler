1	Program → Declaration-list $
2	Declaration-list → Declaration Declaration-list
3	Declaration-list → ε
4	Declaration → Declaration-initial Declaration-prime
5	Declaration-initial → Type-specifier ID
6	Declaration-prime → Fun-declaration-prime
7	Declaration-prime → Var-declaration-prime
8	Var-declaration-prime → ;
9	Var-declaration-prime → [ NUM ] ;
10	Fun-declaration-prime → ( Params ) Compound-stmt
11	Type-specifier → int
12	Type-specifier → void
13	Params → int ID Param-prime Param-list
14	Params → void
15	Param-list → , Param Param-list
16	Param-list → ε
17	Param → Declaration-initial Param-prime
18	Param-prime → [ ]
19	Param-prime → ε
20	Compound-stmt → { Declaration-list Statement-list }
21	Statement-list → Statement Statement-list
22	Statement-list → ε
23	Statement → Expression-stmt
24	Statement → Compound-stmt
25	Statement → Selection-stmt
26	Statement → Iteration-stmt
27	Statement → Return-stmt
28	Expression-stmt → Expression ;
29	Expression-stmt → break ;
30	Expression-stmt → ;
31	Selection-stmt → if ( Expression ) Statement else Statement
32	Iteration-stmt → repeat Statement until ( Expression )
33	Return-stmt → return Return-stmt-prime
34	Return-stmt-prime → ;
35	Return-stmt-prime → Expression ;
36	Expression → Simple-expression-zegond
37	Expression → ID B
38	B → = Expression
39	B → [ Expression ] H
40	B → Simple-expression-prime
41	H → = Expression
42	H → G D C
43	Simple-expression-zegond → Additive-expression-zegond C
44	Simple-expression-prime → Additive-expression-prime C
45	C → Relop Additive-expression
46	C → ε
47	Relop → <
48	Relop → ==
49	Additive-expression → Term D
50	Additive-expression-prime → Term-prime D
51	Additive-expression-zegond → Term-zegond D
52	D → Addop Term D
53	D → ε
54	Addop → +
55	Addop → -
56	Term → Factor G
57	Term-prime → Factor-prime G
58	Term-zegond → Factor-zegond G
59	G → * Factor G
60	G → ε
61	Factor → ( Expression )
62	Factor → ID Var-call-prime
63	Factor → NUM
64	Var-call-prime → ( Args )
65	Var-call-prime → Var-prime
66	Var-prime → [ Expression ]
67	Var-prime → ε
68	Factor-prime → ( Args )
69	Factor-prime → ε
70	Factor-zegond → ( Expression )
71	Factor-zegond → NUM
72	Args → Arg-list
73	Args → ε
74	Arg-list → Expression Arg-list-prime
75	Arg-list-prime → , Expression Arg-list-prime
76	Arg-list-prime → ε