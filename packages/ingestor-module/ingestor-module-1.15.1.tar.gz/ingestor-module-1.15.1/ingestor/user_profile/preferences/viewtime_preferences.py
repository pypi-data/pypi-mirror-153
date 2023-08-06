from graphdb import GraphDb
from ingestor.user_profile.preferences.generate_preferences import PreferenceGenerator
from ingestor.user_profile.main.config import S3_PAYTV_PREFIX, S3_NONPAYTV_PREFIX, DURATION_BINS, TOD_MAPPING
from ingestor.common.read_write_from_s3 import ConnectS3
from ingestor.user_profile.main.post_offline import PostOfflineMain
from ingestor.common.constants import PAY_TV_CONTENT, NO_PAY_TV_CONTENT, CUSTOMER_ID, \
    VIDEO_ID1, CONTENT_ID, DURATION, CSV_EXTENSION, CONTENT_DURATION, TOD, CREATED_ON
from pandas import DataFrame, merge
import logging
logging.basicConfig(level=logging.INFO)

class UserViewTimePreferences:

    @staticmethod
    def get_content_durations(
            graph
    ) -> DataFrame:
        """
        For all the contents dumped into graphDB, identify their
        respective content durations and return the response
        as a dataframe object
        :param graph: graphDB object
        :return: Dataframe object pandas
        """
        response = []
        for content_type in [PAY_TV_CONTENT, NO_PAY_TV_CONTENT]:
            subresponse = graph.custom_query(
                query=f'''g.V().hasLabel('{content_type}').match(
                        __.as("c").values("content_id").as("content_id"),
                        __.as("c").values("duration_minute").as("content_duration")
                        ).select("content_id", "content_duration")''',
                payload={
                    content_type: content_type,
                }
            )
            # flattening the response obtained
            response.extend(
                [item for temp_response in subresponse
                 for item in temp_response]
            )

        return DataFrame(response)

    @staticmethod
    def get_closest_bin(
            value: int,
            bins: list
    ):
        """
        Identify the closest bin to which a value belongs
        :param value: value to be assigned to a bin
        :param bins: list of different bin values
        :return: bin value to which the input should be assigned
        """
        result = [abs(bin_val - value) for bin_val in bins]
        return bins[result.index(min(result))]

    @staticmethod
    def perform_duration_binning(
            duration_df: DataFrame
    ):
        """
        For each value in the content-duration mapping,
        substitute the corresponding bin value
        :param duration_df: Dataframe object pandas
        :return: Dataframe object pandas
        """
        duration_bins = DURATION_BINS
        duration_df[CONTENT_DURATION] = [
            UserViewTimePreferences.get_closest_bin(
                value=duration,
                bins=duration_bins
            )
            for duration in duration_df[CONTENT_DURATION]
        ]
        return duration_df

    @staticmethod
    def get_content_view_tod(
            ubd: DataFrame
    ) -> DataFrame:
        """
        Identify the time of day as per the input
        timestamps in the ubd data
        :param ubd: Dataframe object pandas
        :return: Dataframe object pandas
        """
        content_viewed_tod = DataFrame()
        content_viewed_tod[CUSTOMER_ID] = ubd[CUSTOMER_ID]
        content_viewed_tod[DURATION] = ubd[DURATION]
        content_viewed_tod[TOD] = (ubd[CREATED_ON].dt.hour % 24 + 6) // 6
        content_viewed_tod[TOD].replace(TOD_MAPPING, inplace=True)
        return content_viewed_tod

    @staticmethod
    def get_viewtime_preferences(
            ubd: DataFrame,
            connection_uri,
            resource,
            bucket_name,
            object_name
    ):
        """
        Obtain user-wise time of day and content duration preferences
        based on the log from the UBD Data. This function internally
        utilises the same preference methods as used to generate the
        category, subcategory, actor preferences etc.
        :param ubd: Dataframe object pandas
        :param connection_uri: graphDB connection object
        :param resource: s3 resource object
        :param bucket_name: s3 bucket name
        :param object_name: s3 object name
        :return: Dataframe objects pandas
        """
        graph = GraphDb.from_connection(connection_uri)

        # preparing content duration input data for preference generation
        content_durations = \
            UserViewTimePreferences.get_content_durations(graph=graph)

        binned_content_durations = \
            UserViewTimePreferences.perform_duration_binning(
                content_durations.copy()
            )

        merged_ubd_content_duration = merge(
            ubd[[CUSTOMER_ID, VIDEO_ID1, DURATION]],
            binned_content_durations,
            left_on=VIDEO_ID1,
            right_on=CONTENT_ID,
            how="inner"
        )
        merged_ubd_content_duration.drop(columns=[CONTENT_ID], inplace=True)

        # preparing content view tod input data for preference generation
        content_view_tod = UserViewTimePreferences.get_content_view_tod(ubd=ubd)

        # generating preferences
        preference = PreferenceGenerator(
            feature=TOD,
            feature_cutoff=2,
            user_cutoff=2
        )
        tod_preferences = preference.controller(
            data=content_view_tod,
            resource=resource,
            bucket_name=bucket_name,
            object_name=object_name,
        )
        preference = PreferenceGenerator(
            feature=CONTENT_DURATION,
            feature_cutoff=2,
            user_cutoff=2
        )
        content_duration_preferences = preference.controller(
            data=merged_ubd_content_duration,
            resource=resource,
            bucket_name=bucket_name,
            object_name=object_name,
        )

        return tod_preferences, content_duration_preferences

    @staticmethod
    def generate_mapping_format(
            data: DataFrame,
            resource,
            bucket_name: str,
            object_name: str,
            filename: str,
            users: list,
            is_paytv: bool
    ):
        """
        Reformat the mapping files and save the final result onto S3
        :param data: Dataframe object pandas
        :param resource: s3 resource
        :param bucket_name: s3 bucket name
        :param object_name: s3 object name
        :param filename: the name to be assigned to the file
        required to be uploaded to s3
        :param users: list of users to keep in the final result
        :param is_paytv: boolean indicator for paytv status
        :return: None, the result is uploaded to S3 for further usages
        """
        post_offline = PostOfflineMain(
            s3_resource=resource,
            s3_bucket_name=bucket_name,
            s3_object_name=object_name
        )

        data = post_offline.drop_nan_features(data)
        if len(data.columns) == 1 or len(data) == 0:
            return
        paytv = S3_PAYTV_PREFIX \
            if is_paytv else S3_NONPAYTV_PREFIX

        data = post_offline.filter_users(
            all_users=data,
            users_to_keep=users
        )
        data = post_offline.get_feature_relations(
            data=data
        )
        logging.info(
            "Dumping file " + "mapping_" +
            paytv + filename + CSV_EXTENSION
        )
        ConnectS3().write_csv_to_s3(
            bucket_name=post_offline.s3_bucket_name,
            object_name=post_offline.s3_object_name + "mapping_" +
            paytv + filename + CSV_EXTENSION,
            resource=post_offline.s3_resource,
            df_to_upload=data
        )
