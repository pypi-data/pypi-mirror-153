/* -*- sql -*-

   postgres specific registered procedures,
   require the plpgsql language installed

*/

DROP FUNCTION IF EXISTS comma_join (anyarray) CASCADE;
CREATE FUNCTION comma_join (anyarray) RETURNS text AS $$
    SELECT array_to_string($1, ', ')
$$ LANGUAGE SQL;;


DROP FUNCTION IF EXISTS cw_array_append_unique (anyarray, anyelement) CASCADE;
CREATE FUNCTION cw_array_append_unique (anyarray, anyelement) RETURNS anyarray AS $$
    SELECT CASE WHEN $2=ANY($1) THEN $1 ELSE $1 || $2 END;
$$ LANGUAGE SQL;;

DROP AGGREGATE IF EXISTS group_concat (anyelement) CASCADE;
CREATE AGGREGATE group_concat (
  basetype = anyelement,
  sfunc = cw_array_append_unique,
  stype = anyarray,
  finalfunc = comma_join,
  initcond = '{}'
);;


DROP FUNCTION IF EXISTS limit_size (fulltext text, format text, maxsize integer);
CREATE FUNCTION limit_size (fulltext text, format text, maxsize integer) RETURNS text AS $$
DECLARE
    plaintext text;
BEGIN
    IF char_length(fulltext) < maxsize THEN
       RETURN fulltext;
    END IF;
    IF format = 'text/html' OR format = 'text/xhtml' OR format = 'text/xml' THEN
       plaintext := regexp_replace(fulltext, '<[a-zA-Z/][^>]*>', '', 'g');
    ELSE
       plaintext := fulltext;
    END IF;
    IF char_length(plaintext) < maxsize THEN
       RETURN plaintext;
    ELSE
       RETURN substring(plaintext from 1 for maxsize) || '...';
    END IF;
END
$$ LANGUAGE plpgsql;;

DROP FUNCTION IF EXISTS text_limit_size (fulltext text, maxsize integer);
CREATE FUNCTION text_limit_size (fulltext text, maxsize integer) RETURNS text AS $$
BEGIN
    RETURN limit_size(fulltext, 'text/plain', maxsize);
END
$$ LANGUAGE plpgsql;;
