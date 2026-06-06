# CodeDNA Database Design - Sprint 2

This document details the database schema design for CodeDNA's Skill Intelligence Engine, focusing on how user knowledge, skills, and proficiency are represented.

---

## 1. Naming & Design Conventions
- **Table Names**: Snake-case and pluralized (e.g., `users`, `skills`, `user_skills`).
- **Foreign Keys**: Plural prefix singularized + `_id` suffix (e.g., `user_id` pointing to `users.id`).
- **Cascade Rules**: `ondelete="CASCADE"` is enforced on foreign keys linking to the parent objects. If a user or skill is deleted, the corresponding mapping is automatically deleted to maintain referential integrity.
- **Timestamps**: Explicit timezone-aware `created_at` and `updated_at` fields are utilized where tracking temporal changes is critical.

---

## 2. Table Schemas

### `users` (User Model)
Stores user account credentials and registration info.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key, Autoincrement, Indexed | Unique user identifier. |
| `full_name` | `VARCHAR(255)` | Non-Nullable | The user's full name. |
| `email` | `VARCHAR(255)` | Unique, Non-Nullable | User's email address used for login. |
| `hashed_password`| `VARCHAR(255)` | Non-Nullable | Password hashed via bcrypt. |

#### Relationships:
- `user_skills` (`1 ─── * UserSkill`): Linked to user's skill proficiency entries. Cascades deletes.

---

### `skills` (Skill Model)
A curated taxonomy of technical topics. These are seeded dynamically via scripts instead of being hardcoded, allowing CodeDNA's knowledge graph to scale.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key, Autoincrement, Indexed | Unique skill identifier. |
| `name` | `VARCHAR(100)` | Unique, Non-Nullable, Indexed | Name of the skill (e.g., `Python`, `FastAPI`, `Docker`). |
| `category` | `VARCHAR(100)` | Non-Nullable, Indexed | High-level category (e.g., `Programming`, `Backend`, `DevOps`). |
| `description` | `VARCHAR(500)` | Nullable | A short description detailing what the skill covers. |
| `created_at` | `TIMESTAMP` | Timezone-Aware, Default: `NOW()` | Timestamp when the skill was added. |

#### Standard Categories:
To support smart roadmap generation and categorization, the skills are categorized into:
- `Programming`
- `Backend`
- `Frontend`
- `DSA`
- `Database`
- `System Design`
- `DevOps`
- `AI/ML`
- `Cloud`

#### Relationships:
- `user_skills` (`1 ─── * UserSkill`): List of user proficiencies mapping to this skill. Cascades deletes.

---

### `user_skills` (UserSkill Association Model)
An association table with metadata linking `User` and `Skill`. This acts as the Core Knowledge Graph mapping a user's proficiency.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key, Autoincrement, Indexed | Unique record identifier. |
| `user_id` | `INTEGER` | FK (`users.id`), Non-Nullable, Indexed | Link to the user. |
| `skill_id` | `INTEGER` | FK (`skills.id`), Non-Nullable, Indexed | Link to the skill. |
| `level` | `INTEGER` | Default: `1`, Range: `[1, 10]` | Proficiency level (1 = Beginner, 10 = Expert). |
| `confidence` | `INTEGER` | Default: `1`, Range: `[1, 10]` | Confidence level in user's assessment of this skill. |
| `created_at` | `TIMESTAMP` | Timezone-Aware, Default: `NOW()` | Initial assessment date. |
| `updated_at` | `TIMESTAMP` | Timezone-Aware, Default: `NOW()`, Updates on Change | Last assessment/level update date. |

#### Constraints:
- `chk_user_skills_level`: `CheckConstraint("level >= 1 AND level <= 10")`
- `chk_user_skills_confidence`: `CheckConstraint("confidence >= 1 AND confidence <= 10")`
- `uq_user_skill`: `UniqueConstraint("user_id", "skill_id")` - Prevents duplicate entries of a single skill for any user.

#### Relationships:
- `user` (`* ─── 1 User`): Resolves to the corresponding user object.
- `skill` (`* ─── 1 Skill`): Resolves to the corresponding skill object.

---

## 3. System Design & Future Scalability

### Scalability Considerations:
1. **Index Optimization**:
   - Unique and index constraints are defined on `name` and `category` in `skills` to optimize lookups when searching and filtering skills.
   - Database indexes are placed on `user_id` and `skill_id` inside `user_skills` to guarantee fast joins when looking up a user's knowledge profile.
2. **Learning Analytics & Velocity**:
   - The inclusion of timezone-aware `created_at` and `updated_at` fields in `user_skills` enables tracking of learning progress over time.
   - We can calculate learning velocity (e.g., how quickly a user progresses from Level 2 to Level 5) by tracking the difference between update intervals.
3. **Graph Traversal & Recommendations**:
   - In subsequent sprints, we can layer a recommendations engine (e.g., collaborative filtering or graph-based recommendations) directly on top of the `user_skills` association table.
