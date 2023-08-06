import pandas as pd
from ingestor.common.constants import CONTENT_ID, CATEGORY_ID, SUBCATEGORY_ID, \
    CATEGORY, SUBCATEGORY, ACTORS, TAGS, TAGS_ID, CUSTOMER_ID, DURATION,\
    COUNTRY_ID, REGION_NAME, DEVOPS, \
    VIDEO_ID1, ATTRIBUTE1, CATEGORY1, CATEGORY2, ACTOR_ID, DIRECTORS, DIRECTOR_ID, \
    LEFT, CREATED_ON,VIDEO_ID2




class UserMap:
    @staticmethod
    def preprocessing_ubd(ubd_chunk=None):
        ubd_chunk = ubd_chunk[ubd_chunk['customer_id'].notnull()]
        ubd_chunk[CUSTOMER_ID] = ubd_chunk[CUSTOMER_ID].astype(str)
        ubd_chunk[CREATED_ON] = pd.to_datetime(ubd_chunk[CREATED_ON],unit='s')
        ubd_chunk[COUNTRY_ID] = ubd_chunk[COUNTRY_ID].astype(str)
        ubd_chunk[REGION_NAME] = ubd_chunk[REGION_NAME].astype(str)
        ubd_chunk[DEVOPS] = ubd_chunk[DEVOPS].astype(str)
        ubd_chunk[ATTRIBUTE1] = ubd_chunk[ATTRIBUTE1].astype(str)
        ubd_chunk = ubd_chunk[~ubd_chunk[VIDEO_ID1].str.contains(',', na=False)]
        ubd_chunk[VIDEO_ID1] = ubd_chunk[VIDEO_ID1].astype(int)
        ubd_chunk[VIDEO_ID2] = ubd_chunk[VIDEO_ID2].fillna(-1)
        ubd_chunk[VIDEO_ID2] = ubd_chunk[VIDEO_ID2].astype(int)
        ubd_chunk[DURATION] = ubd_chunk[DURATION].astype(int)
        ubd_chunk = UserMap.fetch_prepare_category(ubd_chunk=ubd_chunk)
        ubd_chunk = UserMap.fetch_prepare_subcategory(ubd_chunk=ubd_chunk)
        return ubd_chunk

    @staticmethod
    def fetch_prepare_category(ubd_chunk=None):
        ubd_chunk = ubd_chunk[pd.to_numeric(ubd_chunk[CATEGORY1], errors='coerce').notnull()]

        ubd_chunk[CATEGORY] = ubd_chunk[CATEGORY1].apply(lambda x: [{CATEGORY_ID: int(float(x))}])
        ubd_chunk = ubd_chunk.drop(CATEGORY1, axis=1)
        return ubd_chunk

    @staticmethod
    def fetch_prepare_subcategory(ubd_chunk=None):
        ubd_chunk = ubd_chunk[pd.to_numeric(ubd_chunk[CATEGORY2], errors='coerce').notnull()]
        ubd_chunk[SUBCATEGORY] = ubd_chunk[CATEGORY2].apply(lambda x: [{SUBCATEGORY_ID: int(float(x))}])
        ubd_chunk = ubd_chunk.drop(CATEGORY2, axis=1)
        return ubd_chunk

    @staticmethod
    def prepare_tags(ubd_chunk, df_content_having_tag):
        tag = df_content_having_tag.groupby([CONTENT_ID])[TAGS_ID].apply(list).reset_index(name=TAGS_ID)

        tags_df = pd.merge(ubd_chunk, tag, left_on=VIDEO_ID1, right_on=CONTENT_ID,
                           how=LEFT)

        tags_df = tags_df[tags_df[TAGS_ID].notnull()]
        tags_df[TAGS] = tags_df[TAGS_ID].apply(lambda x: [{TAGS_ID: int(i)} for i in x])
        tags_df = tags_df.drop([CONTENT_ID, TAGS_ID], axis=1)
        return tags_df

    @staticmethod
    def prepare_actor(ubd_chunk, df_content_having_actor):
        actor = df_content_having_actor.groupby([CONTENT_ID])[ACTOR_ID].apply(list).reset_index(name=ACTOR_ID)

        actor_df = pd.merge(ubd_chunk, actor, left_on=VIDEO_ID1, right_on=CONTENT_ID,
                            how=LEFT)

        actor_df = actor_df[actor_df[ACTOR_ID].notnull()]
        actor_df[ACTORS] = actor_df[ACTOR_ID].apply(lambda x: [{ACTOR_ID: i} for i in x])
        actor_df = actor_df.drop([CONTENT_ID, ACTOR_ID], axis=1)
        return actor_df

    @staticmethod
    def prepare_director(ubd_chunk, df_content_having_actor):
        director = df_content_having_actor.groupby([CONTENT_ID])[ACTOR_ID].apply(list).reset_index(name=DIRECTOR_ID)

        director_df = pd.merge(ubd_chunk, director, left_on=VIDEO_ID1, right_on=CONTENT_ID,
                               how=LEFT)

        director_df = director_df[director_df[DIRECTOR_ID].notnull()]
        director_df[DIRECTORS] = director_df[DIRECTOR_ID].apply(lambda x: [{DIRECTOR_ID: i} for i in x])
        director_df = director_df.drop([CONTENT_ID, DIRECTOR_ID], axis=1)
        return director_df

    @staticmethod
    def mapping_ubd(ubd_chunk=None, tag_data=None, actor_data=None,
                    director_data=None):
        ubd_chunk = UserMap.preprocessing_ubd(ubd_chunk)
        ubd_chunk = UserMap.prepare_tags(ubd_chunk, tag_data)
        ubd_chunk = UserMap.prepare_actor(ubd_chunk, actor_data)
        ubd_chunk = UserMap.prepare_director(ubd_chunk, director_data)
        return ubd_chunk


