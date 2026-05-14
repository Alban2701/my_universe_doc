ALTER TABLE
    "universe"
ALTER COLUMN
    "creator_id" DROP NOT NULL;

ALTER TABLE
    "entities"
ALTER COLUMN
    "creator_id" DROP NOT NULL;

ALTER TABLE
    "text_blocks"
ALTER COLUMN
    "creator_id" DROP NOT NULL;

ALTER TABLE
    "comments"
ALTER COLUMN
    "creator_id" DROP NOT NULL;

ALTER TABLE
    "commits"
ALTER COLUMN
    "creator_id" DROP NOT NULL;

ALTER TABLE
    "invitations" DROP CONSTRAINT IF EXISTS invitations_universe_id_fkey,
ADD
    CONSTRAINT invitations_universe_id_fkey FOREIGN KEY ("universe_id") REFERENCES "universe" ("id") ON DELETE CASCADE;

ALTER TABLE
    "entities" DROP CONSTRAINT IF EXISTS entities_universe_id_fkey,
ADD
    CONSTRAINT entities_universe_id_fkey FOREIGN KEY ("universe_id") REFERENCES "universe" ("id") ON DELETE CASCADE;

ALTER TABLE
    "user_universe" DROP CONSTRAINT IF EXISTS user_universe_universe_id_fkey,
ADD
    CONSTRAINT user_universe_universe_id_fkey FOREIGN KEY ("universe_id") REFERENCES "universe" ("id") ON DELETE CASCADE;

ALTER TABLE
    "text_blocks" DROP CONSTRAINT IF EXISTS text_blocks_entity_id_fkey,
ADD
    CONSTRAINT text_blocks_entity_id_fkey FOREIGN KEY ("entity_id") REFERENCES "entities" ("id") ON DELETE CASCADE;

ALTER TABLE
    "comments" DROP CONSTRAINT IF EXISTS comments_entity_id_fkey,
ADD
    CONSTRAINT comments_entity_id_fkey FOREIGN KEY ("entity_id") REFERENCES "entities" ("id") ON DELETE CASCADE;

ALTER TABLE
    "user_entity" DROP CONSTRAINT IF EXISTS user_entity_entity_id_fkey,
ADD
    CONSTRAINT user_entity_entity_id_fkey FOREIGN KEY ("entity_id") REFERENCES "entities" ("id") ON DELETE CASCADE;

ALTER TABLE
    "comments" DROP CONSTRAINT IF EXISTS comments_text_block_id_fkey,
ADD
    CONSTRAINT comments_text_block_id_fkey FOREIGN KEY ("text_block_id") REFERENCES "text_blocks" ("id") ON DELETE CASCADE;

ALTER TABLE
    "user_text_block" DROP CONSTRAINT IF EXISTS user_text_block_text_block_id_fkey,
ADD
    CONSTRAINT user_text_block_text_block_id_fkey FOREIGN KEY ("text_block_id") REFERENCES "text_blocks" ("id") ON DELETE CASCADE;

ALTER TABLE
    "comments" DROP CONSTRAINT IF EXISTS comments_comment_id_fkey,
ADD
    CONSTRAINT comments_comment_id_fkey FOREIGN KEY ("comment_id") REFERENCES "comments" ("id") ON DELETE CASCADE;

ALTER TABLE
    "universe" DROP CONSTRAINT IF EXISTS universe_creator_id_fkey,
ADD
    CONSTRAINT universe_creator_id_fkey FOREIGN KEY ("creator_id") REFERENCES "users" ("id") ON DELETE
SET
    NULL;

ALTER TABLE
    "invitations" DROP CONSTRAINT IF EXISTS invitations_sender_id_fkey,
ADD
    CONSTRAINT invitations_sender_id_fkey FOREIGN KEY ("sender_id") REFERENCES "users" ("id") ON DELETE CASCADE;

ALTER TABLE
    "invitations" DROP CONSTRAINT IF EXISTS invitations_receiver_id_fkey,
ADD
    CONSTRAINT invitations_receiver_id_fkey FOREIGN KEY ("receiver_id") REFERENCES "users" ("id") ON DELETE CASCADE;

ALTER TABLE
    "entities" DROP CONSTRAINT IF EXISTS entities_creator_id_fkey,
ADD
    CONSTRAINT entities_creator_id_fkey FOREIGN KEY ("creator_id") REFERENCES "users" ("id") ON DELETE
SET
    NULL;

ALTER TABLE
    "text_blocks" DROP CONSTRAINT IF EXISTS text_blocks_creator_id_fkey,
ADD
    CONSTRAINT text_blocks_creator_id_fkey FOREIGN KEY ("creator_id") REFERENCES "users" ("id") ON DELETE
SET
    NULL;

ALTER TABLE
    "comments" DROP CONSTRAINT IF EXISTS comments_creator_id_fkey,
ADD
    CONSTRAINT comments_creator_id_fkey FOREIGN KEY ("creator_id") REFERENCES "users" ("id") ON DELETE
SET
    NULL;

ALTER TABLE
    "commits" DROP CONSTRAINT IF EXISTS commits_creator_id_fkey,
ADD
    CONSTRAINT commits_creator_id_fkey FOREIGN KEY ("creator_id") REFERENCES "users" ("id") ON DELETE
SET
    NULL;

ALTER TABLE
    "user_universe" DROP CONSTRAINT IF EXISTS user_universe_user_id_fkey,
ADD
    CONSTRAINT user_universe_user_id_fkey FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;

ALTER TABLE
    "user_text_block" DROP CONSTRAINT IF EXISTS user_text_block_user_id_fkey,
ADD
    CONSTRAINT user_text_block_user_id_fkey FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;

ALTER TABLE
    "user_entity" DROP CONSTRAINT IF EXISTS user_entity_user_id_fkey,
ADD
    CONSTRAINT user_entity_user_id_fkey FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;

ALTER TABLE
    "session_token" DROP CONSTRAINT IF EXISTS session_token_user_id_fkey,
ADD
    CONSTRAINT session_token_user_id_fkey FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE;