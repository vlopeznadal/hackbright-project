--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: favorites; Type: TABLE; Schema: public; Owner: virginialopeznadal
--

CREATE TABLE public.favorites (
    query_id integer NOT NULL,
    user_id integer,
    cafe_id character varying(50) NOT NULL,
    cafe_name character varying(50) NOT NULL,
    image_url character varying(100),
    cafe_street character varying(50) NOT NULL,
    cafe_city character varying(50) NOT NULL,
    cafe_state character varying(50) NOT NULL,
    cafe_zip character varying(50) NOT NULL
);


ALTER TABLE public.favorites OWNER TO virginialopeznadal;

--
-- Name: favorites_query_id_seq; Type: SEQUENCE; Schema: public; Owner: virginialopeznadal
--

CREATE SEQUENCE public.favorites_query_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.favorites_query_id_seq OWNER TO virginialopeznadal;

--
-- Name: favorites_query_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: virginialopeznadal
--

ALTER SEQUENCE public.favorites_query_id_seq OWNED BY public.favorites.query_id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: virginialopeznadal
--

CREATE TABLE public.reviews (
    review_id integer NOT NULL,
    user_id integer,
    date timestamp without time zone NOT NULL,
    rating integer NOT NULL,
    review character varying(500)
);


ALTER TABLE public.reviews OWNER TO virginialopeznadal;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: virginialopeznadal
--

CREATE SEQUENCE public.reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_review_id_seq OWNER TO virginialopeznadal;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: virginialopeznadal
--

ALTER SEQUENCE public.reviews_review_id_seq OWNED BY public.reviews.review_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: virginialopeznadal
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(50) NOT NULL
);


ALTER TABLE public.users OWNER TO virginialopeznadal;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: virginialopeznadal
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO virginialopeznadal;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: virginialopeznadal
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: favorites query_id; Type: DEFAULT; Schema: public; Owner: virginialopeznadal
--

ALTER TABLE ONLY public.favorites ALTER COLUMN query_id SET DEFAULT nextval('public.favorites_query_id_seq'::regclass);


--
-- Name: reviews review_id; Type: DEFAULT; Schema: public; Owner: virginialopeznadal
--

ALTER TABLE ONLY public.reviews ALTER COLUMN review_id SET DEFAULT nextval('public.reviews_review_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: virginialopeznadal
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: virginialopeznadal
--

COPY public.favorites (query_id, user_id, cafe_id, cafe_name, image_url, cafe_street, cafe_city, cafe_state, cafe_zip) FROM stdin;
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: virginialopeznadal
--

COPY public.reviews (review_id, user_id, date, rating, review) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: virginialopeznadal
--

COPY public.users (user_id, email, password) FROM stdin;
\.


--
-- Name: favorites_query_id_seq; Type: SEQUENCE SET; Schema: public; Owner: virginialopeznadal
--

SELECT pg_catalog.setval('public.favorites_query_id_seq', 1, false);


--
-- Name: reviews_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: virginialopeznadal
--

SELECT pg_catalog.setval('public.reviews_review_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: virginialopeznadal
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: favorites favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: virginialopeznadal
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (query_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: virginialopeznadal
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: virginialopeznadal
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: virginialopeznadal
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: favorites favorites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: virginialopeznadal
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: reviews reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: virginialopeznadal
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

