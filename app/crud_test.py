import asyncio
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_helper import db_helper
from app.core import User, Profile, Post


# simple create request. Прямое обращение к модели к одному атрибуту
async def create_user(session: AsyncSession, name: str) -> User:
    user = User(name=name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    print("user", user)
    return user


# query запрос с фильтром по атрибуту
async def get_user_by_name(session: AsyncSession, name: str) -> User | None:
    query = select(User).where(User.name == name)
    # result: Result = await session.execute(query)
    # user: User | None = result.scalar_one_or_none()
    user = await session.scalar(query)  # пропускает execute()
    print(user)
    return user


# simple create query через model(несколько атрибутов)
async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    name: str | None = None,
    surname: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        name=name,
        surname=surname,
    )
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


# asyncio не подгружает профиль, если транзакция завершена, нужен options(joiinedload(User.profile))
async def get_user_profiles(session: AsyncSession):
    query = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(query)
    # users = result.scalars(query)
    users = await session.scalars(query)
    for user in users:
        print(user)
        print(user.profile.name)


# create request через генератор, создает несколько постов, которые переданы через *post_titles
# !!! осторожно с именнованными атрибутами и позиционными !!!
async def create_post(
    session: AsyncSession,
    user_id: int,
    *post_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


# разница запросом с joinedload(sesion.scalars()), jointedload(session.execute) и selectinload
async def get_users_posts(
    session: AsyncSession,
):
    # query = select(User).options(joinedload(User.posts)).order_by(User.id)
    # users = await session.scalars(query)
    # for user in users.unique():
    #     print(user)
    #     for post in user.posts:
    #         print("- ", post)

    # query = select(User).options(joinedload(User.posts)).order_by(User.id)
    # result: Result = await session.execute(query)
    # users = result.unique().scalars()
    # for user in users:
    #     print(user)
    #     for post in user.posts:
    #         print("- ", post)

    query = (
        select(User).options(selectinload(User.posts)).order_by(User.id)
    )  # вместе с selectinload и без unique()
    users = await session.scalars(query)
    for user in users:  # type: User
        print(user)
        for post in user.posts:
            print("- ", post)


# joinedload хорошо работает для подгрузки к одному, для подгрузки один ко многим нужно использовать unique
async def get_posts_with_authors(session: AsyncSession):
    query = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(query)
    for post in posts:  # type: Post
        print(post)
        print("author: ", post.user)


# selectinload - это тоже join
# selectinload хорошо работает для подрузки один ко многим,
# минус, что делает дополнительный запрос, но избалвяет от дублирования в запросе
async def get_users_with_posts_and_profiles(session: AsyncSession):
    query = (
        select(User)
        .options(joinedload(User.profile), selectinload(User.posts))
        .order_by(User.id)
    )
    users = await session.scalars(query)
    for user in users:
        print(user)
        print(user.profile and user.profile.name)
        for post in user.posts:
            print("- ", post)


# запрос со вложенным join: joiin(Prifile.user).joinedload(Profile.user).selectinload(User.posts)
async def get_profiles_with_users_with_posts(session: AsyncSession):
    query = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .where(User.name == "Ann")
        .order_by(Profile.id)
    )
    profiles = await session.scalars(query)
    for profile in profiles:
        print(profile.name, profile.user)
        print(profile.user.posts)


async def test_requests(session: AsyncSession):
    # await create_user(session=session, name="John")
    # await create_user(session=session, name="Ann")
    # # await create_user(session=session, name="Elly")
    # user_ann = await get_user_by_name(session=session, name="Ann")
    # user_john = await get_user_by_name(session=session, name="John")
    # await create_user_profile(
    #     session=session,
    #     user_id=user_ann.id,
    #     name="Ann",
    # )
    # await create_user_profile(
    #     session=session,
    #     user_id=user_john.id,
    #     surname="Lee",
    # )
    # # await get_user_profiles(session=session)
    # await create_post(session, user_ann.id, "SQLAlchemy", "Python", "FastApi")
    # await create_post(session, user_john.id, "Redis", "POSTGRES")
    # await get_users_posts(session=session)
    # await get_posts_with_authors(session)
    # await get_users_with_posts_and_profiles(session)
    # await get_profiles_with_users_with_posts(session
    pass


async def demo_m2m(session: AsyncSession):
    pass


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
