# User Login Database Schema

## Tables

### User
- `id` (UUID, Primary Key)
- `username` (String, Unique, Not Null)
- `email` (String, Unique, Not Null)
- `password_hash` (String, Not Null)
- `salt` (String, Not Null)
- `created_at` (Timestamp, Not Null)
- `updated_at` (Timestamp, Not Null)
- `last_login` (Timestamp)
- `is_active` (Boolean, Default: True)

### Role
- `id` (UUID, Primary Key)
- `name` (String, Unique, Not Null)
- `description` (String)

### User_Role
- `user_id` (UUID, Foreign Key to User)
- `role_id` (UUID, Foreign Key to Role)
- `assigned_at` (Timestamp, Not Null)

### Session
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key to User)
- `token` (String, Not Null)
- `created_at` (Timestamp, Not Null)
- `expires_at` (Timestamp, Not Null)
- `ip_address` (String)
- `user_agent` (String)

## Security
- All passwords hashed with bcrypt
- Sensitive data encrypted at rest
- Session tokens cryptographically random

## Indexes
- Index on `username` and `email` for fast lookups
- Index on `user_id` in Session table
- Index on `token` in Session table