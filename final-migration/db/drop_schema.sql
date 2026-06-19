-- ============================================================
-- drop_schema.sql
-- Wipes all tables for a clean re-apply of 001_initial_schema.sql
-- Development only — never run in production
-- ============================================================

drop function if exists increment_variation_total_sales(uuid, int);
drop function if exists increment_product_total_sales(uuid, int);
drop table if exists order_items cascade;
drop table if exists orders cascade;
drop table if exists bookmarks cascade;
drop table if exists cart_items cascade;
drop table if exists admins cascade;
drop table if exists product_description_images cascade;
drop table if exists description_images cascade;
drop table if exists variation_images cascade;
drop table if exists product_images cascade;
drop table if exists variations cascade;
drop table if exists product_categories cascade;
drop table if exists products cascade;
drop table if exists categories cascade;
drop table if exists brands cascade;
