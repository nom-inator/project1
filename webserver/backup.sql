--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: address; Type: TABLE; Schema: public; Owner: cw2952; Tablespace: 
--

CREATE TABLE address (
    aid text NOT NULL,
    rid text NOT NULL,
    lat numeric,
    lng numeric,
    zip integer,
    city text,
    state text,
    st_addr text,
    cross_st text
);


ALTER TABLE public.address OWNER TO cw2952;

--
-- Name: condition; Type: TABLE; Schema: public; Owner: cw2952; Tablespace: 
--

CREATE TABLE condition (
    cid text NOT NULL,
    day_of_week integer,
    weather text,
    "time" text,
    CONSTRAINT condition_day_of_week_check CHECK ((0 < day_of_week)),
    CONSTRAINT condition_day_of_week_check1 CHECK ((day_of_week < 8)),
    CONSTRAINT condition_time_check CHECK (("time" = ANY (ARRAY['breakfast'::text, 'lunch'::text, 'dinner'::text]))),
    CONSTRAINT condition_weather_check CHECK ((weather = ANY (ARRAY['clear'::text, 'rainy'::text, 'snowy'::text, 'cloudy'::text])))
);


ALTER TABLE public.condition OWNER TO cw2952;

--
-- Name: favouriteslist; Type: TABLE; Schema: public; Owner: cw2952; Tablespace: 
--

CREATE TABLE favouriteslist (
    listid text NOT NULL,
    uid text NOT NULL
);


ALTER TABLE public.favouriteslist OWNER TO cw2952;

--
-- Name: restaurant; Type: TABLE; Schema: public; Owner: cw2952; Tablespace: 
--

CREATE TABLE restaurant (
    rid text NOT NULL,
    rname text NOT NULL,
    aid text NOT NULL,
    rate integer NOT NULL,
    CONSTRAINT restaurant_rate_check CHECK (((-1) < rate)),
    CONSTRAINT restaurant_rate_check1 CHECK ((rate < 6))
);


ALTER TABLE public.restaurant OWNER TO cw2952;

--
-- Name: restaurantoflist; Type: TABLE; Schema: public; Owner: cw2952; Tablespace: 
--

CREATE TABLE restaurantoflist (
    rid text NOT NULL,
    listid text NOT NULL
);


ALTER TABLE public.restaurantoflist OWNER TO cw2952;

--
-- Name: user_location; Type: TABLE; Schema: public; Owner: cw2952; Tablespace: 
--

CREATE TABLE user_location (
    lid text NOT NULL,
    uid text,
    lat numeric,
    lng numeric
);


ALTER TABLE public.user_location OWNER TO cw2952;

--
-- Name: users; Type: TABLE; Schema: public; Owner: cw2952; Tablespace: 
--

CREATE TABLE users (
    uid text NOT NULL,
    name text,
    lid text
);


ALTER TABLE public.users OWNER TO cw2952;

--
-- Name: visit; Type: TABLE; Schema: public; Owner: cw2952; Tablespace: 
--

CREATE TABLE visit (
    rid text NOT NULL,
    cid text NOT NULL,
    count integer,
    CONSTRAINT visit_count_check CHECK ((count > (-1)))
);


ALTER TABLE public.visit OWNER TO cw2952;

--
-- Data for Name: address; Type: TABLE DATA; Schema: public; Owner: cw2952
--

COPY address (aid, rid, lat, lng, zip, city, state, st_addr, cross_st) FROM stdin;
a1	r1	40.806051	-73.965824	10025	New York	NY	2895 Broadway	113th and Broadway
a2	r2	40.807344	-73.964817	10025	New York	NY	2937 Broadway	115th and Broadway
a3	r3	40.805962	-73.96582	10025	New York	NY	2893 Broadway	113th and Broadway
a4	r4	40.803244	-73.966759	10025	New York	NY	258 W 109th St	109th and Broadway
a5	r5	40.805465	-73.965391	10025	New York	NY	2880 Broadway	112th and Broadway
a6	r6	40.805212	-73.966391	10025	New York	NY	2867 Broadway	111th and Broadway
a7	r7	40.803227	-73.963979	10025	New York	NY	1020 Amsterdam Ave	110th and Amsterdam
a8	r8	40.810265	-73.961835	10025	New York	NY	550 W 120th St	120th and Broadway
a9	r9	40.806901	-73.963661	10027	New York	NY	2920 Broadway	114th and Broadway
a10	r10	40.805892	-73.962419	10027	New York	NY	511 W. 114th Street	114th and Amsterdam
\.


--
-- Data for Name: condition; Type: TABLE DATA; Schema: public; Owner: cw2952
--

COPY condition (cid, day_of_week, weather, "time") FROM stdin;
c1	1	clear	breakfast
c2	1	rainy	breakfast
c3	1	snowy	breakfast
c4	1	cloudy	breakfast
c5	1	clear	lunch
c6	1	rainy	lunch
c7	1	snowy	lunch
c8	1	cloudy	lunch
c9	1	clear	dinner
c10	1	rainy	dinner
c11	1	snowy	dinner
c12	1	cloudy	dinner
c13	2	clear	breakfast
c14	2	rainy	breakfast
c15	2	snowy	breakfast
c16	2	cloudy	breakfast
c17	2	clear	lunch
c18	2	rainy	lunch
c19	2	snowy	lunch
c20	2	cloudy	lunch
c21	2	clear	dinner
c22	2	rainy	dinner
c23	2	snowy	dinner
c24	2	cloudy	dinner
c25	3	clear	breakfast
c26	3	rainy	breakfast
c27	3	snowy	breakfast
c28	3	cloudy	breakfast
c29	3	clear	lunch
c30	3	rainy	lunch
c31	3	snowy	lunch
c32	3	cloudy	lunch
c33	3	clear	dinner
c34	3	rainy	dinner
c35	3	snowy	dinner
c36	3	cloudy	dinner
c37	4	clear	breakfast
c38	4	rainy	breakfast
c39	4	snowy	breakfast
c40	4	cloudy	breakfast
c41	4	clear	lunch
c42	4	rainy	lunch
c43	4	snowy	lunch
c44	4	cloudy	lunch
c45	4	clear	dinner
c46	4	rainy	dinner
c47	4	snowy	dinner
c48	4	cloudy	dinner
c49	5	clear	breakfast
c50	5	rainy	breakfast
c51	5	snowy	breakfast
c52	5	cloudy	breakfast
c53	5	clear	lunch
c54	5	rainy	lunch
c55	5	snowy	lunch
c56	5	cloudy	lunch
c57	5	clear	dinner
c58	5	rainy	dinner
c59	5	clear	dinner
c60	5	rainy	dinner
c61	6	snowy	breakfast
c62	6	cloudy	breakfast
c63	6	clear	breakfast
c64	6	rainy	breakfast
c65	6	snowy	lunch
c66	6	cloudy	lunch
c67	6	clear	lunch
c68	6	rainy	lunch
c69	6	clear	dinner
c70	6	rainy	dinner
c71	6	snowy	dinner
c72	6	cloudy	dinner
c73	7	clear	breakfast
c74	7	rainy	breakfast
c75	7	snowy	breakfast
c76	7	cloudy	breakfast
c77	7	clear	lunch
c78	7	rainy	lunch
c79	7	clear	lunch
c80	7	rainy	lunch
c81	7	snowy	dinner
c82	7	cloudy	dinner
c83	7	clear	dinner
c84	7	rainy	dinner
\.


--
-- Data for Name: favouriteslist; Type: TABLE DATA; Schema: public; Owner: cw2952
--

COPY favouriteslist (listid, uid) FROM stdin;
list1	bob999
list2	angel88
list3	mike
list4	stvn
list5	mary0704
list6	ewu
list7	evanj
list8	pmann
list9	tombrady
list10	queenbeeftw
\.


--
-- Data for Name: restaurant; Type: TABLE DATA; Schema: public; Owner: cw2952
--

COPY restaurant (rid, rname, aid, rate) FROM stdin;
r1	The Saltshaker	a1	3
r2	doucevert	a2	3
r3	Neighbourhood	a3	2
r4	Myth	a4	1
r5	Bobby's	a5	0
r6	The Penthouse	a6	0
r7	1030	a7	4
r8	Jo's Coffee	a8	0
r9	West Cafe	a9	1
r10	KK's Place	a10	2
\.


--
-- Data for Name: restaurantoflist; Type: TABLE DATA; Schema: public; Owner: cw2952
--

COPY restaurantoflist (rid, listid) FROM stdin;
r10	list1
r7	list2
r9	list3
r3	list4
r2	list5
r1	list6
r8	list7
r9	list10
r5	list2
r7	list10
\.


--
-- Data for Name: user_location; Type: TABLE DATA; Schema: public; Owner: cw2952
--

COPY user_location (lid, uid, lat, lng) FROM stdin;
l1	bob999	40.806051	-73.965824
l2	angel88	40.807344	-73.964817
l3	mike	40.805962	-73.96582
l4	stvn	40.803244	-73.966759
l5	mary0704	40.805465	-73.965391
l6	ewu	40.805212	-73.966391
l7	evanj	40.803227	-73.963979
l8	pmann	40.810265	-73.961835
l9	tombrady	40.806901	-73.963661
l10	queenbeeftw	40.805892	-73.962419
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: cw2952
--

COPY users (uid, name, lid) FROM stdin;
bob999	Bob	l1
angel88	Angel	l2
mike	Mike	l3
stvn	Steven	l4
mary0704	Mary	l5
ewu	Eugene	l6
evanj	Evan	l7
pmann	Peyton Manning	l8
tombrady	Tom Brady	l9
queenbeeftw	Beyonc̩	l10
\.


--
-- Data for Name: visit; Type: TABLE DATA; Schema: public; Owner: cw2952
--

COPY visit (rid, cid, count) FROM stdin;
r1	c29	4743
r2	c30	4308
r3	c31	1749
r4	c32	4116
r5	c33	2552
r6	c34	959
r7	c35	2389
r8	c36	259
r9	c37	3144
r10	c38	4727
r1	c39	2475
r2	c40	642
r3	c41	2287
r4	c42	3850
r5	c43	84
r6	c44	1677
r7	c45	2267
r8	c46	2640
r9	c2	971
r10	c3	3897
r1	c4	4441
r2	c5	737
r3	c6	3082
r4	c7	1499
r5	c8	2509
r6	c9	4851
r7	c10	1099
r8	c11	1132
r9	c12	585
r10	c13	862
\.


--
-- Name: address_pkey; Type: CONSTRAINT; Schema: public; Owner: cw2952; Tablespace: 
--

ALTER TABLE ONLY address
    ADD CONSTRAINT address_pkey PRIMARY KEY (aid, rid);


--
-- Name: condition_pkey; Type: CONSTRAINT; Schema: public; Owner: cw2952; Tablespace: 
--

ALTER TABLE ONLY condition
    ADD CONSTRAINT condition_pkey PRIMARY KEY (cid);


--
-- Name: favouriteslist_pkey; Type: CONSTRAINT; Schema: public; Owner: cw2952; Tablespace: 
--

ALTER TABLE ONLY favouriteslist
    ADD CONSTRAINT favouriteslist_pkey PRIMARY KEY (listid);


--
-- Name: restaurant_pkey; Type: CONSTRAINT; Schema: public; Owner: cw2952; Tablespace: 
--

ALTER TABLE ONLY restaurant
    ADD CONSTRAINT restaurant_pkey PRIMARY KEY (rid);


--
-- Name: restaurantoflist_pkey; Type: CONSTRAINT; Schema: public; Owner: cw2952; Tablespace: 
--

ALTER TABLE ONLY restaurantoflist
    ADD CONSTRAINT restaurantoflist_pkey PRIMARY KEY (rid, listid);


--
-- Name: user_location_pkey; Type: CONSTRAINT; Schema: public; Owner: cw2952; Tablespace: 
--

ALTER TABLE ONLY user_location
    ADD CONSTRAINT user_location_pkey PRIMARY KEY (lid);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: cw2952; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: visit_pkey; Type: CONSTRAINT; Schema: public; Owner: cw2952; Tablespace: 
--

ALTER TABLE ONLY visit
    ADD CONSTRAINT visit_pkey PRIMARY KEY (rid, cid);


--
-- Name: arfk; Type: FK CONSTRAINT; Schema: public; Owner: cw2952
--

ALTER TABLE ONLY restaurant
    ADD CONSTRAINT arfk FOREIGN KEY (aid, rid) REFERENCES address(aid, rid) MATCH FULL;


--
-- Name: favouriteslist_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cw2952
--

ALTER TABLE ONLY favouriteslist
    ADD CONSTRAINT favouriteslist_uid_fkey FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE;


--
-- Name: lfk; Type: FK CONSTRAINT; Schema: public; Owner: cw2952
--

ALTER TABLE ONLY users
    ADD CONSTRAINT lfk FOREIGN KEY (lid) REFERENCES user_location(lid) MATCH FULL;


--
-- Name: restaurantoflist_listid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cw2952
--

ALTER TABLE ONLY restaurantoflist
    ADD CONSTRAINT restaurantoflist_listid_fkey FOREIGN KEY (listid) REFERENCES favouriteslist(listid) ON DELETE CASCADE;


--
-- Name: restaurantoflist_rid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cw2952
--

ALTER TABLE ONLY restaurantoflist
    ADD CONSTRAINT restaurantoflist_rid_fkey FOREIGN KEY (rid) REFERENCES restaurant(rid) ON DELETE CASCADE;


--
-- Name: rfk; Type: FK CONSTRAINT; Schema: public; Owner: cw2952
--

ALTER TABLE ONLY address
    ADD CONSTRAINT rfk FOREIGN KEY (rid) REFERENCES restaurant(rid) MATCH FULL ON DELETE CASCADE;


--
-- Name: user_location_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cw2952
--

ALTER TABLE ONLY user_location
    ADD CONSTRAINT user_location_uid_fkey FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE;


--
-- Name: visit_cid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cw2952
--

ALTER TABLE ONLY visit
    ADD CONSTRAINT visit_cid_fkey FOREIGN KEY (cid) REFERENCES condition(cid) ON DELETE CASCADE;


--
-- Name: visit_rid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cw2952
--

ALTER TABLE ONLY visit
    ADD CONSTRAINT visit_rid_fkey FOREIGN KEY (rid) REFERENCES restaurant(rid) ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;
GRANT USAGE ON SCHEMA public TO grader;


--
-- Name: address; Type: ACL; Schema: public; Owner: cw2952
--

REVOKE ALL ON TABLE address FROM PUBLIC;
REVOKE ALL ON TABLE address FROM cw2952;
GRANT ALL ON TABLE address TO cw2952;
GRANT SELECT ON TABLE address TO grader;


--
-- Name: condition; Type: ACL; Schema: public; Owner: cw2952
--

REVOKE ALL ON TABLE condition FROM PUBLIC;
REVOKE ALL ON TABLE condition FROM cw2952;
GRANT ALL ON TABLE condition TO cw2952;
GRANT SELECT ON TABLE condition TO grader;


--
-- Name: favouriteslist; Type: ACL; Schema: public; Owner: cw2952
--

REVOKE ALL ON TABLE favouriteslist FROM PUBLIC;
REVOKE ALL ON TABLE favouriteslist FROM cw2952;
GRANT ALL ON TABLE favouriteslist TO cw2952;
GRANT SELECT ON TABLE favouriteslist TO grader;


--
-- Name: restaurant; Type: ACL; Schema: public; Owner: cw2952
--

REVOKE ALL ON TABLE restaurant FROM PUBLIC;
REVOKE ALL ON TABLE restaurant FROM cw2952;
GRANT ALL ON TABLE restaurant TO cw2952;
GRANT SELECT ON TABLE restaurant TO grader;


--
-- Name: restaurantoflist; Type: ACL; Schema: public; Owner: cw2952
--

REVOKE ALL ON TABLE restaurantoflist FROM PUBLIC;
REVOKE ALL ON TABLE restaurantoflist FROM cw2952;
GRANT ALL ON TABLE restaurantoflist TO cw2952;
GRANT SELECT ON TABLE restaurantoflist TO grader;


--
-- Name: user_location; Type: ACL; Schema: public; Owner: cw2952
--

REVOKE ALL ON TABLE user_location FROM PUBLIC;
REVOKE ALL ON TABLE user_location FROM cw2952;
GRANT ALL ON TABLE user_location TO cw2952;
GRANT SELECT ON TABLE user_location TO grader;


--
-- Name: users; Type: ACL; Schema: public; Owner: cw2952
--

REVOKE ALL ON TABLE users FROM PUBLIC;
REVOKE ALL ON TABLE users FROM cw2952;
GRANT ALL ON TABLE users TO cw2952;
GRANT SELECT ON TABLE users TO grader;


--
-- Name: visit; Type: ACL; Schema: public; Owner: cw2952
--

REVOKE ALL ON TABLE visit FROM PUBLIC;
REVOKE ALL ON TABLE visit FROM cw2952;
GRANT ALL ON TABLE visit TO cw2952;
GRANT SELECT ON TABLE visit TO grader;


--
-- PostgreSQL database dump complete
--

