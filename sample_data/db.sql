--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: tw2
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer NOT NULL,
    accepted boolean DEFAULT false
);


ALTER TABLE public.answer ;

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: tw2
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answer_id_seq ;

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tw2
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: tw2
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer NOT NULL
);


ALTER TABLE public.comment ;

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: tw2
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_id_seq ;

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tw2
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: tw2
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);


ALTER TABLE public.question ;

--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: tw2
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_id_seq ;

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tw2
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: tw2
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.question_tag ;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: tw2
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


ALTER TABLE public.tag ;

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: tw2
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq ;

--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tw2
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    password character varying NOT NULL,
    reg_date timestamp(6) without time zone DEFAULT now() NOT NULL,
    reputation integer DEFAULT 0
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: tw2
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image, user_id, accepted) FROM stdin;
2	2017-04-25 14:42:00	35	1	Look it up in the Python docs	images/image2.jpg	0	f
3	2019-09-24 11:04:49	8	1	sajt		0	f
4	2019-09-24 11:05:30	13	1	sajt		0	f
5	2019-09-24 15:08:42	0	0	sanyi		0	f
6	2019-09-25 10:47:03	0	1	asd''asd		0	f
7	2019-09-25 10:47:29	0	1	''a		0	f
8	2019-09-25 10:48:47	0	1	a''1		0	f
9	2019-09-25 10:51:21	0	3	a'1		0	f
10	2019-09-25 13:53:01	1	2	bump		0	f
1	2019-09-25 14:16:42	4	1	You need to use brackets: my_list = [] changed -----		0	f
11	2019-09-26 11:02:47	0	5	sajt		0	f
12	2019-09-26 11:02:55	0	5	sajt2		0	f
13	2019-09-26 13:28:16	0	4	salata		0	f
14	2019-09-26 14:27:16	0	6	nanaaaaaaaan		0	f
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: tw2
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) FROM stdin;
73	1	\N	asd	2019-09-25 14:48:11	\N	0
2	\N	1	I think you could use my_list = list() as well.	2017-05-02 16:55:00	\N	0
4	\N	2	asdsa	2019-09-24 11:29:23	\N	0
5	\N	2	asdsa	2019-09-24 11:32:29	\N	0
6	2	\N	asdas	2019-09-24 11:37:48	\N	0
7	2	\N	asdsada	2019-09-24 11:38:15	\N	0
68	1	\N	sajotskeksz 3	2019-09-25 13:26:20	2	0
11	\N	1	sadsad	2019-09-24 11:40:05	\N	0
22	\N	1	bliblubla	2019-09-24 13:29:56	2	0
16	2	\N	asdas	2019-09-24 13:17:55	\N	0
76	\N	1	komment edit	2019-09-26 12:51:10	1	0
77	1	\N	komment q edit	2019-09-26 12:51:20	1	0
34	\N	4	asdsa	2019-09-24 14:50:51	\N	0
79	\N	3	asdsa	2019-09-26 13:20:45	\N	0
82	\N	7	aaaaaaaaaaaaaaaaqqqqqqqqqqqqq	2019-09-26 13:26:56	\N	0
85	\N	13	nokedli + porkolt	2019-09-26 13:28:24	1	0
45	\N	4	asdsasdsa	2019-09-24 14:59:37	\N	0
46	\N	4	asdsasdsa	2019-09-24 15:00:06	\N	0
31	\N	4	123 edited hope it owrks	2019-09-24 14:48:44	1	0
49	\N	4	asdsadsad	2019-09-24 15:03:19	\N	0
87	5	\N	asdsad	2019-09-26 14:41:18	\N	0
51	\N	2	asdsa	2019-09-24 15:04:44	\N	0
88	5	\N	asdsa	2019-09-26 14:43:27	\N	0
89	\N	1	gdsvsdv	2019-09-27 13:45:42	\N	0
57	\N	5	asdsadas	2019-09-24 15:10:54	\N	0
58	\N	5	sajt	2019-09-25 09:39:09	\N	0
59	\N	5	sajtsdfds	2019-09-25 09:39:48	\N	0
63	1	\N	as'asdsa	2019-09-25 10:46:37	\N	0
65	3	\N	a'1	2019-09-25 10:51:27	\N	0
66	\N	5	new comment test #1	2019-09-25 11:11:42	\N	0
64	1	\N	asd	2019-09-25 10:48:37	\N	0
61	0	\N	asd	2019-09-25 10:34:48	\N	0
12	1	\N	123asd123	2019-09-24 11:42:07	\N	0
14	1	\N	asd	2019-09-24 13:08:58	\N	0
19	1	\N	asdsad	2019-09-24 13:21:06	\N	0
20	1	\N	selele	2019-09-24 13:21:14	\N	0
21	1	\N	asdasdsadzxcxzc	2019-09-24 13:29:38	\N	0
15	2	\N	alma lama	2019-09-24 13:10:00	\N	0
18	2	\N	asd	2019-09-24 13:20:58	2	0
17	2	\N	sadsadas	2019-09-24 13:19:41	1	0
3	2	\N	lajos	2019-09-24 11:27:46	1	0
69	\N	10	sajt	2019-09-25 13:56:41	1	0
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: tw2
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image, user_id) FROM stdin;
1	2019-09-25 10:47:48	15	9	Wordpress loading multiple jQuery Versions	I'asd developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();\r\n\r\nI could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.\r\n\r\nBUT in my theme i also using jquery via webpack so the loading order is now following:\r\n\r\njquery\r\nbooklet\r\napp.js (bundled file with webpack, including jquery)		0
3	2019-09-25 10:53:11	0	0	asd'12	qwe'%123		0
0	2017-04-28 08:29:00	29	8	How to make lists in Python?	I am totally new to this, any hints?	\N	0
2	2017-05-01 10:41:00	1364	62	Drawing canvas with an image picked with Cordova Camera Plugin	I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS, it throws errors such as cross origin issue, or that I'm trying to use an unknown format.\n	\N	0
4	2019-09-25 17:23:31	0	0	sadsa	asdsad		0
5	2019-09-25 17:23:36	0	0	asdasd	asqdas		0
6	2019-09-26 17:21:03	0	0	1234	12345	images/Screenshot from 2019-07-04 14-41-52.png	0
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: tw2
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
0	1
1	3
2	3
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: tw2
--

COPY public.tag (id, name) FROM stdin;
1	python
2	sql
3	css
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, password, reg_date, reputation) FROM stdin;
0	Admin	$2b$12$WnD.WnpkstOjJ942BWBNDOavvV1txRHaV3O27uRVge9.6tyuFtSRW	2019-10-07 00:00:00	0
1	user	$2b$12$1hSkXN6wc5xagujdbP2DEeXmj4MUisS2bX5dLcl.bJMH5eEJnh962	2019-10-07 00:00:00	0
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tw2
--

SELECT pg_catalog.setval('public.answer_id_seq', 14, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tw2
--

SELECT pg_catalog.setval('public.comment_id_seq', 89, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tw2
--

SELECT pg_catalog.setval('public.question_id_seq', 6, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tw2
--

SELECT pg_catalog.setval('public.tag_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- Name: answer fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: comment fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: question fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: tw2
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer NOT NULL,
    accepted boolean DEFAULT false
);


--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer NOT NULL
);


--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);


--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


--
-- Name: tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    password character varying NOT NULL,
    reg_date timestamp(6) without time zone DEFAULT now() NOT NULL,
    reputation integer DEFAULT 0
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image, user_id, accepted) FROM stdin;
2	2017-04-25 14:42:00	35	1	Look it up in the Python docs	images/image2.jpg	0	f
3	2019-09-24 11:04:49	8	1	sajt		0	f
4	2019-09-24 11:05:30	13	1	sajt		0	f
5	2019-09-24 15:08:42	0	0	sanyi		0	f
6	2019-09-25 10:47:03	0	1	asd''asd		0	f
7	2019-09-25 10:47:29	0	1	''a		0	f
8	2019-09-25 10:48:47	0	1	a''1		0	f
9	2019-09-25 10:51:21	0	3	a'1		0	f
10	2019-09-25 13:53:01	1	2	bump		0	f
1	2019-09-25 14:16:42	4	1	You need to use brackets: my_list = [] changed -----		0	f
11	2019-09-26 11:02:47	0	5	sajt		0	f
12	2019-09-26 11:02:55	0	5	sajt2		0	f
13	2019-09-26 13:28:16	0	4	salata		0	f
14	2019-09-26 14:27:16	0	6	nanaaaaaaaan		0	f
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) FROM stdin;
73	1	\N	asd	2019-09-25 14:48:11	\N	0
2	\N	1	I think you could use my_list = list() as well.	2017-05-02 16:55:00	\N	0
4	\N	2	asdsa	2019-09-24 11:29:23	\N	0
5	\N	2	asdsa	2019-09-24 11:32:29	\N	0
6	2	\N	asdas	2019-09-24 11:37:48	\N	0
7	2	\N	asdsada	2019-09-24 11:38:15	\N	0
68	1	\N	sajotskeksz 3	2019-09-25 13:26:20	2	0
11	\N	1	sadsad	2019-09-24 11:40:05	\N	0
22	\N	1	bliblubla	2019-09-24 13:29:56	2	0
16	2	\N	asdas	2019-09-24 13:17:55	\N	0
76	\N	1	komment edit	2019-09-26 12:51:10	1	0
77	1	\N	komment q edit	2019-09-26 12:51:20	1	0
34	\N	4	asdsa	2019-09-24 14:50:51	\N	0
79	\N	3	asdsa	2019-09-26 13:20:45	\N	0
82	\N	7	aaaaaaaaaaaaaaaaqqqqqqqqqqqqq	2019-09-26 13:26:56	\N	0
85	\N	13	nokedli + porkolt	2019-09-26 13:28:24	1	0
45	\N	4	asdsasdsa	2019-09-24 14:59:37	\N	0
46	\N	4	asdsasdsa	2019-09-24 15:00:06	\N	0
31	\N	4	123 edited hope it owrks	2019-09-24 14:48:44	1	0
49	\N	4	asdsadsad	2019-09-24 15:03:19	\N	0
87	5	\N	asdsad	2019-09-26 14:41:18	\N	0
51	\N	2	asdsa	2019-09-24 15:04:44	\N	0
88	5	\N	asdsa	2019-09-26 14:43:27	\N	0
89	\N	1	gdsvsdv	2019-09-27 13:45:42	\N	0
57	\N	5	asdsadas	2019-09-24 15:10:54	\N	0
58	\N	5	sajt	2019-09-25 09:39:09	\N	0
59	\N	5	sajtsdfds	2019-09-25 09:39:48	\N	0
63	1	\N	as'asdsa	2019-09-25 10:46:37	\N	0
65	3	\N	a'1	2019-09-25 10:51:27	\N	0
66	\N	5	new comment test #1	2019-09-25 11:11:42	\N	0
64	1	\N	asd	2019-09-25 10:48:37	\N	0
61	0	\N	asd	2019-09-25 10:34:48	\N	0
12	1	\N	123asd123	2019-09-24 11:42:07	\N	0
14	1	\N	asd	2019-09-24 13:08:58	\N	0
19	1	\N	asdsad	2019-09-24 13:21:06	\N	0
20	1	\N	selele	2019-09-24 13:21:14	\N	0
21	1	\N	asdasdsadzxcxzc	2019-09-24 13:29:38	\N	0
15	2	\N	alma lama	2019-09-24 13:10:00	\N	0
18	2	\N	asd	2019-09-24 13:20:58	2	0
17	2	\N	sadsadas	2019-09-24 13:19:41	1	0
3	2	\N	lajos	2019-09-24 11:27:46	1	0
69	\N	10	sajt	2019-09-25 13:56:41	1	0
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image, user_id) FROM stdin;
1	2019-09-25 10:47:48	15	9	Wordpress loading multiple jQuery Versions	I'asd developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();\r\n\r\nI could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.\r\n\r\nBUT in my theme i also using jquery via webpack so the loading order is now following:\r\n\r\njquery\r\nbooklet\r\napp.js (bundled file with webpack, including jquery)		0
3	2019-09-25 10:53:11	0	0	asd'12	qwe'%123		0
0	2017-04-28 08:29:00	29	8	How to make lists in Python?	I am totally new to this, any hints?	\N	0
2	2017-05-01 10:41:00	1364	62	Drawing canvas with an image picked with Cordova Camera Plugin	I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS, it throws errors such as cross origin issue, or that I'm trying to use an unknown format.\n	\N	0
4	2019-09-25 17:23:31	0	0	sadsa	asdsad		0
5	2019-09-25 17:23:36	0	0	asdasd	asqdas		0
6	2019-09-26 17:21:03	0	0	1234	12345	images/Screenshot from 2019-07-04 14-41-52.png	0
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
0	1
1	3
2	3
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tag (id, name) FROM stdin;
1	python
2	sql
3	css
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, name, password, reg_date, reputation) FROM stdin;
0	Admin	admin	2019-10-07 00:00:00	0
1	user	user	2019-10-07 00:00:00	0
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.answer_id_seq', 14, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.comment_id_seq', 89, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.question_id_seq', 6, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tag_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- Name: answer fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: comment fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: question fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.question DROP CONSTRAINT fk_user_id;
ALTER TABLE ONLY public.comment DROP CONSTRAINT fk_user_id;
ALTER TABLE ONLY public.answer DROP CONSTRAINT fk_user_id;
ALTER TABLE ONLY public.question_tag DROP CONSTRAINT fk_tag_id;
ALTER TABLE ONLY public.comment DROP CONSTRAINT fk_question_id;
ALTER TABLE ONLY public.question_tag DROP CONSTRAINT fk_question_id;
ALTER TABLE ONLY public.answer DROP CONSTRAINT fk_question_id;
ALTER TABLE ONLY public.comment DROP CONSTRAINT fk_answer_id;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_name_key;
ALTER TABLE ONLY public.tag DROP CONSTRAINT pk_tag_id;
ALTER TABLE ONLY public.question_tag DROP CONSTRAINT pk_question_tag_id;
ALTER TABLE ONLY public.question DROP CONSTRAINT pk_question_id;
ALTER TABLE ONLY public.comment DROP CONSTRAINT pk_comment_id;
ALTER TABLE ONLY public.answer DROP CONSTRAINT pk_answer_id;
ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.tag ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.question ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.comment ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.answer ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.users_id_seq;
DROP TABLE public.users;
DROP SEQUENCE public.tag_id_seq;
DROP TABLE public.tag;
DROP TABLE public.question_tag;
DROP SEQUENCE public.question_id_seq;
DROP TABLE public.question;
DROP SEQUENCE public.comment_id_seq;
DROP TABLE public.comment;
DROP SEQUENCE public.answer_id_seq;
DROP TABLE public.answer;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_id integer NOT NULL,
    accepted boolean DEFAULT false
);


--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer NOT NULL
);


--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_id integer
);


--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


--
-- Name: tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    password character varying NOT NULL,
    reg_date timestamp(6) without time zone DEFAULT now() NOT NULL,
    reputation integer DEFAULT 0
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image, user_id, accepted) FROM stdin;
2	2017-04-25 14:42:00	35	1	Look it up in the Python docs	images/image2.jpg	0	f
3	2019-09-24 11:04:49	8	1	sajt		0	f
4	2019-09-24 11:05:30	13	1	sajt		0	f
5	2019-09-24 15:08:42	0	0	sanyi		0	f
6	2019-09-25 10:47:03	0	1	asd''asd		0	f
7	2019-09-25 10:47:29	0	1	''a		0	f
8	2019-09-25 10:48:47	0	1	a''1		0	f
9	2019-09-25 10:51:21	0	3	a'1		0	f
10	2019-09-25 13:53:01	1	2	bump		0	f
1	2019-09-25 14:16:42	4	1	You need to use brackets: my_list = [] changed -----		0	f
11	2019-09-26 11:02:47	0	5	sajt		0	f
12	2019-09-26 11:02:55	0	5	sajt2		0	f
13	2019-09-26 13:28:16	0	4	salata		0	f
14	2019-09-26 14:27:16	0	6	nanaaaaaaaan		0	f
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) FROM stdin;
73	1	\N	asd	2019-09-25 14:48:11	\N	0
2	\N	1	I think you could use my_list = list() as well.	2017-05-02 16:55:00	\N	0
4	\N	2	asdsa	2019-09-24 11:29:23	\N	0
5	\N	2	asdsa	2019-09-24 11:32:29	\N	0
6	2	\N	asdas	2019-09-24 11:37:48	\N	0
7	2	\N	asdsada	2019-09-24 11:38:15	\N	0
68	1	\N	sajotskeksz 3	2019-09-25 13:26:20	2	0
11	\N	1	sadsad	2019-09-24 11:40:05	\N	0
22	\N	1	bliblubla	2019-09-24 13:29:56	2	0
16	2	\N	asdas	2019-09-24 13:17:55	\N	0
76	\N	1	komment edit	2019-09-26 12:51:10	1	0
77	1	\N	komment q edit	2019-09-26 12:51:20	1	0
34	\N	4	asdsa	2019-09-24 14:50:51	\N	0
79	\N	3	asdsa	2019-09-26 13:20:45	\N	0
82	\N	7	aaaaaaaaaaaaaaaaqqqqqqqqqqqqq	2019-09-26 13:26:56	\N	0
85	\N	13	nokedli + porkolt	2019-09-26 13:28:24	1	0
45	\N	4	asdsasdsa	2019-09-24 14:59:37	\N	0
46	\N	4	asdsasdsa	2019-09-24 15:00:06	\N	0
31	\N	4	123 edited hope it owrks	2019-09-24 14:48:44	1	0
49	\N	4	asdsadsad	2019-09-24 15:03:19	\N	0
87	5	\N	asdsad	2019-09-26 14:41:18	\N	0
51	\N	2	asdsa	2019-09-24 15:04:44	\N	0
88	5	\N	asdsa	2019-09-26 14:43:27	\N	0
89	\N	1	gdsvsdv	2019-09-27 13:45:42	\N	0
57	\N	5	asdsadas	2019-09-24 15:10:54	\N	0
58	\N	5	sajt	2019-09-25 09:39:09	\N	0
59	\N	5	sajtsdfds	2019-09-25 09:39:48	\N	0
63	1	\N	as'asdsa	2019-09-25 10:46:37	\N	0
65	3	\N	a'1	2019-09-25 10:51:27	\N	0
66	\N	5	new comment test #1	2019-09-25 11:11:42	\N	0
64	1	\N	asd	2019-09-25 10:48:37	\N	0
61	0	\N	asd	2019-09-25 10:34:48	\N	0
12	1	\N	123asd123	2019-09-24 11:42:07	\N	0
14	1	\N	asd	2019-09-24 13:08:58	\N	0
19	1	\N	asdsad	2019-09-24 13:21:06	\N	0
20	1	\N	selele	2019-09-24 13:21:14	\N	0
21	1	\N	asdasdsadzxcxzc	2019-09-24 13:29:38	\N	0
15	2	\N	alma lama	2019-09-24 13:10:00	\N	0
18	2	\N	asd	2019-09-24 13:20:58	2	0
17	2	\N	sadsadas	2019-09-24 13:19:41	1	0
3	2	\N	lajos	2019-09-24 11:27:46	1	0
69	\N	10	sajt	2019-09-25 13:56:41	1	0
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image, user_id) FROM stdin;
1	2019-09-25 10:47:48	15	9	Wordpress loading multiple jQuery Versions	I'asd developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();\r\n\r\nI could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.\r\n\r\nBUT in my theme i also using jquery via webpack so the loading order is now following:\r\n\r\njquery\r\nbooklet\r\napp.js (bundled file with webpack, including jquery)		0
3	2019-09-25 10:53:11	0	0	asd'12	qwe'%123		0
0	2017-04-28 08:29:00	29	8	How to make lists in Python?	I am totally new to this, any hints?	\N	0
2	2017-05-01 10:41:00	1364	62	Drawing canvas with an image picked with Cordova Camera Plugin	I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS, it throws errors such as cross origin issue, or that I'm trying to use an unknown format.\n	\N	0
4	2019-09-25 17:23:31	0	0	sadsa	asdsad		0
5	2019-09-25 17:23:36	0	0	asdasd	asqdas		0
6	2019-09-26 17:21:03	0	0	1234	12345	images/Screenshot from 2019-07-04 14-41-52.png	0
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
0	1
1	3
2	3
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tag (id, name) FROM stdin;
1	python
2	sql
3	css
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, name, password, reg_date, reputation) FROM stdin;
0	Admin	admin	2019-10-07 00:00:00	0
1	user	user	2019-10-07 00:00:00	0
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.answer_id_seq', 14, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.comment_id_seq', 89, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.question_id_seq', 6, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tag_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: users users_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name_key UNIQUE (name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- Name: answer fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: comment fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: question fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

