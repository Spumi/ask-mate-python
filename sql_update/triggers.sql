CREATE OR REPLACE FUNCTION vote_answer_repu() RETURNS TRIGGER AS $vote_answer_repu$
BEGIN
    IF NEW.vote_number > OLD.vote_number THEN
      update users set reputation = reputation + 10 WHERE id = old.user_id;
	ELSE IF NEW.vote_number < OLD.vote_number THEN   
      update users set reputation = reputation - 2 WHERE id = old.user_id;
		END IF;
   END IF;
RETURN NULL; 
END;
$vote_answer_repu$
LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION vote_question_repu() RETURNS TRIGGER AS $vote_question_repu$
BEGIN
    IF NEW.vote_number > OLD.vote_number THEN
      update users set reputation = reputation + 5 WHERE id = old.user_id;
	ELSE IF NEW.vote_number < OLD.vote_number THEN   
      update users set reputation = reputation - 2 WHERE id = old.user_id;
		END IF;
   END IF;
RETURN NULL; 
END;
$vote_question_repu$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION vote_accept_repu() RETURNS TRIGGER AS $vote_accept_repu$
BEGIN
    IF NEW.accepted is true > OLD.accepted is false THEN
      update users set reputation = reputation + 15 WHERE id = old.user_id;
   END IF;
RETURN NULL; 
END;
$vote_accept_repu$
LANGUAGE plpgsql;


CREATE TRIGGER accept_repu
    AFTER UPDATE OF accepted
    ON public.answer
    FOR EACH ROW
    EXECUTE PROCEDURE public.vote_accept_repu();


CREATE TRIGGER answer_repu
    AFTER UPDATE OF vote_number
    ON public.answer
    FOR EACH ROW
    EXECUTE PROCEDURE public.vote_answer_repu();

CREATE TRIGGER question_repu
    AFTER UPDATE OF vote_number
    ON public.question
    FOR EACH ROW
    EXECUTE PROCEDURE public.vote_question_repu();

