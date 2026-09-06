BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "application_id" (
	"effective_client_id"	INTEGER,
	"bundle_id"	TEXT NOT NULL,
	UNIQUE("bundle_id")
);
CREATE TABLE IF NOT EXISTS "application_workspace_state" (
	"pid"	INTEGER,
	"bundle_id"	TEXT NOT NULL,
	"download_id"	INTEGER,
	"expected_phase"	TEXT NOT NULL DEFAULT 0,
	"retry_count"	INTEGER NOT NULL DEFAULT 0,
	"time_updated"	INTEGER NOT NULL DEFAULT 0,
	"transaction_id"	INTEGER,
	UNIQUE("bundle_id"),
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "asset" (
	"pid"	INTEGER,
	"download_id"	INTEGER,
	"asset_order"	INTEGER DEFAULT 0,
	"asset_type"	TEXT,
	"bytes_total"	INTEGER,
	"url"	TEXT,
	"local_path"	TEXT,
	"destination_url"	TEXT,
	"path_extension"	TEXT,
	"retry_count"	INTEGER,
	"http_method"	TEXT,
	"initial_odr_size"	INTEGER,
	"is_discretionary"	INTEGER DEFAULT 0,
	"is_downloaded"	INTEGER DEFAULT 0,
	"is_drm_free"	INTEGER DEFAULT 0,
	"is_external"	INTEGER DEFAULT 0,
	"is_hls"	INTEGER DEFAULT 0,
	"is_local_cache_server"	INTEGER DEFAULT 0,
	"is_zip_streamable"	INTEGER DEFAULT 0,
	"processing_types"	INTEGER DEFAULT 0,
	"video_dimensions"	TEXT,
	"timeout_interval"	REAL,
	"store_flavor"	TEXT,
	"download_token"	INTEGER DEFAULT 0,
	"blocked_reason"	INTEGER DEFAULT 0,
	"avfoundation_blocked"	INTEGER DEFAULT 0,
	"service_type"	INTEGER DEFAULT 0,
	"protection_type"	INTEGER DEFAULT 0,
	"store_download_key"	TEXT,
	"etag"	TEXT,
	"bytes_to_hash"	INTEGER,
	"hash_type"	INTEGER DEFAULT 0,
	"server_guid"	TEXT,
	"file_protection"	TEXT,
	"variant_id"	TEXT,
	"hash_array"	BLOB,
	"http_headers"	BLOB,
	"request_parameters"	BLOB,
	"body_data"	BLOB,
	"body_data_file_path"	TEXT,
	"sinfs_data"	BLOB,
	"dpinfo_data"	BLOB,
	"uncompressed_size"	INTEGER DEFAULT 0,
	"url_session_task_id"	INTEGER DEFAULT -1,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "canceled_preorder" (
	"pid"	INTEGER,
	"store_account_id"	INTEGER NOT NULL DEFAULT 0,
	"store_item_id"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "client" (
	"pid"	INTEGER,
	"audit_token_data"	BLOB,
	"client_type"	INTEGER DEFAULT 0,
	"client_id"	TEXT NOT NULL,
	UNIQUE("client_id"),
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "download" (
	"pid"	INTEGER,
	"airplay_content_type"	TEXT,
	"artist_name"	TEXT,
	"artwork_is_prerendered"	INTEGER DEFAULT 0,
	"artwork_template_name"	TEXT,
	"auto_update_time"	INTEGER,
	"beta_external_version_identifier"	INTEGER DEFAULT 0,
	"bundle_id"	TEXT,
	"bundle_version"	TEXT,
	"cancel_if_duplicate"	INTEGER DEFAULT 0,
	"cancel_on_failure"	INTEGER DEFAULT 0,
	"cancel_url"	TEXT,
	"client_id"	TEXT,
	"collection_artist_name"	TEXT,
	"collection_group_count"	INTEGER,
	"collection_item_count"	INTEGER,
	"collection_name"	TEXT,
	"composer_name"	TEXT,
	"diverted_job_id"	INTEGER,
	"document_target_id"	TEXT,
	"download_permalink"	TEXT,
	"duet_transfer_type"	INTEGER DEFAULT 0,
	"duration_in_ms"	INTEGER DEFAULT 0,
	"effective_client_id"	INTEGER DEFAULT 0,
	"enable_extensions"	INTEGER DEFAULT 0,
	"episode_id"	TEXT,
	"episode_sort_id"	INTEGER,
	"handler_id"	INTEGER DEFAULT 0,
	"has_4k"	INTEGER DEFAULT 0,
	"has_dolby_vision"	INTEGER DEFAULT 0,
	"has_hdr"	INTEGER DEFAULT 0,
	"has_messages_extension"	INTEGER DEFAULT 0,
	"hls_playlist_url"	TEXT,
	"genre_name"	TEXT,
	"index_in_collection"	INTEGER DEFAULT 0,
	"index_in_collection_group"	INTEGER,
	"is_automatic"	INTEGER DEFAULT 0,
	"is_compilation"	INTEGER DEFAULT 0,
	"is_device_based_vpp"	INTEGER DEFAULT 0,
	"is_diverted"	INTEGER DEFAULT 0,
	"is_explicit"	INTEGER DEFAULT 0,
	"is_from_store"	INTEGER DEFAULT 0,
	"is_hd"	INTEGER DEFAULT 0,
	"is_hls"	INTEGER DEFAULT 0,
	"is_premium"	INTEGER DEFAULT 0,
	"is_private"	INTEGER DEFAULT 0,
	"is_purchase"	INTEGER DEFAULT 0,
	"is_redownload"	INTEGER DEFAULT 0,
	"is_restore"	INTEGER DEFAULT 0,
	"is_rental"	INTEGER DEFAULT 0,
	"is_sample"	INTEGER DEFAULT 0,
	"is_shared"	INTEGER DEFAULT 0,
	"is_store_queued"	INTEGER DEFAULT 0,
	"is_tv_template"	INTEGER DEFAULT 0,
	"is_music_show"	INTEGER DEFAULT 0,
	"kind"	TEXT,
	"launch_prohibited"	INTEGER DEFAULT 0,
	"library_id"	TEXT,
	"loading_priority"	REAL,
	"long_description"	TEXT,
	"long_season_description"	TEXT,
	"messages_artwork_url"	TEXT,
	"network_name"	TEXT,
	"order_key"	DOUBLE DEFAULT 0,
	"order_seed"	INTEGER DEFAULT 0,
	"override_audit_token_data"	BLOB,
	"page_progression_direction"	TEXT,
	"podcast_episode_guid"	TEXT,
	"podcast_feed_url"	TEXT,
	"podcast_type"	TEXT,
	"policy_id"	INTEGER DEFAULT 0,
	"priority"	INTEGER DEFAULT 0,
	"preferred_asset_flavor"	TEXT,
	"purchase_id"	INTEGER DEFAULT 0,
	"rate_limit"	INTEGER,
	"reason"	INTEGER DEFAULT 0,
	"ref_app"	TEXT,
	"ref_url"	TEXT,
	"release_date"	INTEGER,
	"release_year"	INTEGER,
	"rental_id"	INTEGER,
	"resource_timeout_interval"	REAL,
	"season_number"	INTEGER,
	"series_name"	TEXT,
	"software_type"	TEXT,
	"short_description"	TEXT,
	"show_composer"	INTEGER DEFAULT 0,
	"suppress_error_dialogs"	INTEGER NOT NULL DEFAULT 0,
	"store_account_id"	INTEGER,
	"store_account_name"	TEXT,
	"store_artist_id"	INTEGER,
	"store_cohort"	TEXT,
	"store_collection_id"	INTEGER,
	"store_composer_id"	INTEGER,
	"store_download_key"	TEXT,
	"store_front_id"	TEXT,
	"store_genre_id"	INTEGER,
	"store_item_id"	INTEGER,
	"store_match_status"	INTEGER NOT NULL DEFAULT 0,
	"store_publication_version"	INTEGER DEFAULT 0,
	"store_preorder_id"	INTEGER,
	"store_purchase_date"	INTEGER,
	"store_redownload_parameters"	TEXT,
	"store_redownload_status"	INTEGER NOT NULL DEFAULT 0,
	"store_saga_id"	INTEGER,
	"store_software_version_id"	INTEGER,
	"store_transaction_id"	TEXT,
	"store_url"	TEXT,
	"store_xid"	TEXT,
	"thumbnail_newsstand_binding_edge"	TEXT,
	"thumbnail_newsstand_binding_type"	TEXT,
	"thumbnail_url"	TEXT,
	"timeout_interval"	REAL,
	"timestamp"	INTEGER DEFAULT (strftime('%s', 'now')),
	"title"	TEXT,
	"transaction_id"	INTEGER DEFAULT 0,
	"variant_id"	TEXT,
	"work_name"	TEXT,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "download_policy" (
	"pid"	INTEGER,
	"policy_data"	BLOB,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "download_state" (
	"pid"	INTEGER,
	"download_id"	INTEGER,
	"phase"	TEXT,
	"is_restricted"	INTEGER DEFAULT 0,
	"restore_state"	INTEGER DEFAULT 0,
	"blocked_reason"	INTEGER NOT NULL DEFAULT 0,
	"can_pause"	INTEGER DEFAULT 1,
	"can_cancel"	INTEGER DEFAULT 1,
	"can_prioritize"	INTEGER DEFAULT 1,
	"is_server_finished"	INTEGER DEFAULT 0,
	"has_restore_data"	INTEGER DEFAULT -1,
	"last_odr_action"	INTEGER DEFAULT 0,
	"restore_data_size"	INTEGER DEFAULT 0,
	"store_queue_refresh_count"	INTEGER DEFAULT 0,
	"did_restore_data"	INTEGER DEFAULT 0,
	"auto_update_state"	INTEGER NOT NULL DEFAULT 0,
	"download_error"	BLOB,
	"restore_error"	BLOB,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "finished_download" (
	"pid"	INTEGER,
	"finish_url"	TEXT,
	"store_account_id"	INTEGER NOT NULL,
	"store_item_id"	INTEGER,
	"store_transaction_id"	TEXT,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "persistent_download" (
	"download_id"	INTEGER,
	"manager_id"	INTEGER,
	PRIMARY KEY("download_id","manager_id")
);
CREATE TABLE IF NOT EXISTS "persistent_manager" (
	"pid"	INTEGER,
	"client_id"	TEXT,
	"filters_external_downloads"	INTEGER DEFAULT 0,
	"migration_version"	INTEGER DEFAULT 0,
	"wake_up_on_finish"	INTEGER DEFAULT 0,
	"persistence_id"	TEXT,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "persistent_manager_kind" (
	"pid"	INTEGER,
	"manager_id"	INTEGER,
	"download_kind"	TEXT,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "preorder" (
	"pid"	INTEGER,
	"artist_name"	TEXT,
	"kind"	TEXT,
	"release_date"	INTEGER,
	"release_date_string"	TEXT,
	"store_account_id"	INTEGER,
	"store_item_id"	INTEGER,
	"store_preorder_id"	INTEGER,
	"title"	TEXT,
	"image_collection_data"	BLOB,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "purchase" (
	"pid"	INTEGER,
	"batch_id"	INTEGER DEFAULT 0,
	"client_id"	INTEGER DEFAULT 0,
	"order_id"	DOUBLE DEFAULT 0,
	"state"	INTEGER DEFAULT 0,
	"encoded_data"	BLOB,
	"encoded_error"	BLOB,
	"encoded_response"	BLOB,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "purchase_manager" (
	"pid"	INTEGER,
	"client_id_header"	TEXT,
	"manager_id"	TEXT,
	"process_id"	TEXT,
	"url_bag_type"	TEXT,
	PRIMARY KEY("pid")
);
CREATE TABLE IF NOT EXISTS "trnsaction" (
	"pid"	INTEGER,
	"bundle_id"	TEXT,
	"type"	INTEGER DEFAULT 0,
	PRIMARY KEY("pid")
);
INSERT INTO "application_id" VALUES (1,'com.apple.AppStore');
INSERT INTO "application_id" VALUES (3,'com.apple.iBooks');
INSERT INTO "application_id" VALUES (2,'com.apple.MobileStore');
INSERT INTO "application_id" VALUES (4,'com.apple.Music');
INSERT INTO "application_id" VALUES (2,'com.apple.videos');
INSERT INTO "asset" VALUES (0,6936249076851270152,0,'media',3574,'https://is1-ssl.mbstatic.com/image/thumb/Purple221/v4/72/3c/07/1dce85c0-0bcd-acd5-47d6-4586e1084462/c1069db4-2e8e-5510-d774-5df877fad10e.rgb.png/logo_apple_2025_q4_color-0-1x_U007emarketing-0-0-0-7-0-0-0-85-220-0.png','/private/var/containers/Shared/SystemGroup/FC2F2F78-41F6-4774-A4C6-CBD58F32B5C4/Documents/BLDatabaseManager/BLDatabaseManager.sqlite-wal',NULL,'epub',6,'GET',NULL,0,0,0,1,0,0,0,0,NULL,NULL,NULL,5064370024,0,0,0,0,'',NULL,NULL,0,NULL,NULL,NULL,X'62706c6973743030a1015f10203661653866393331356434376135343633623838383164386334653331356166080a000000000000010100000000000000020000000000000000000000000000002d',NULL,NULL,NULL,NULL,NULL,NULL,9656,-1);
INSERT INTO "asset" VALUES (1234567893,6936249076851270153,0,'media',3574,'BACKEND_URL','TARGET_PATH',NULL,'epub',6,'GET',NULL,0,0,0,1,0,0,0,0,NULL,NULL,NULL,5064370024,0,0,0,0,'',NULL,NULL,0,NULL,NULL,NULL,X'62706c6973743030a1015f10203661653866393331356434376135343633623838383164386334653331356166080a000000000000010100000000000000020000000000000000000000000000002d',NULL,NULL,NULL,NULL,NULL,NULL,9656,-1);
INSERT INTO "client" VALUES (-3800587330446784669,X'fffffffff5010000f5010000f5010000f50100001116000000000000be350000',1,'com.apple.MobileStore');
INSERT INTO "client" VALUES (6865578698268706056,X'fffffffff5010000f5010000f5010000f5010000c21400000000000026320000',1,'com.apple.Music');
INSERT INTO "download" VALUES (6936249076851270150,NULL,'Lorde',0,NULL,NULL,0,NULL,NULL,0,0,'https://p19-buy.itunes.apple.com/WebObjects/MZFastFinance.woa/wa/songDownloadDone?download-id=J19N_S_190099478929076&cancel=1','com.apple.iBooks','Lorde',1,11,'Virgin','Ella Marija Lani Yelich-O''Connor, James Harmon Stack & Andrew Aged',NULL,NULL,NULL,0,257066,2,0,NULL,3,0,0,0,0,0,'https://aod.itunes.apple.com/itunes-assets/HLSMusic221/v4/dd/ab/c4/ddabc4d6-35b8-1f0b-d558-b0c0493a2ed8/P1145527675_default.m3u8','Pop',3,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,'ebook',0,NULL,NULL,NULL,NULL,NULL,NULL,100.0,387328,NULL,NULL,NULL,NULL,NULL,-482028619515353839,1,NULL,5785377740721354521,NULL,0,NULL,NULL,772718400,2025,NULL,NULL,NULL,'Virgin',NULL,NULL,0,0,17551287442,NULL,602767352,NULL,1810905299,442404459,'','143509',14,1810905308,0,0,0,772702549,'productType=S&price=0&salableAdamId=1810905308&pricingParameters=HQRDL',128,NULL,NULL,'J19N_S_190099478929076',NULL,'Universal:isrc:NZUM72500022',NULL,NULL,'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/72/3c/07/723c07a7-4ff6-b052-927d-6997fff13676/25UMGIM60545.rgb.jpg/170x170bb.jpg',NULL,1751284926,'Shapeshifter',1966791522949379453,NULL,NULL);
INSERT INTO "download" VALUES (6936249076851270151,NULL,'Lorde',0,NULL,NULL,0,NULL,NULL,0,0,'https://p19-buy.itunes.apple.com/WebObjects/MZFastFinance.woa/wa/songDownloadDone?download-id=J19N_S_190099478929076&cancel=1','com.apple.iBooks','Lorde',1,11,'Virgin','Ella Marija Lani Yelich-O''Connor, James Harmon Stack & Andrew Aged',NULL,NULL,NULL,0,257066,2,0,NULL,3,0,0,0,0,0,'https://aod.itunes.apple.com/itunes-assets/HLSMusic221/v4/dd/ab/c4/ddabc4d6-35b8-1f0b-d558-b0c0493a2ed8/P1145527675_default.m3u8','Pop',3,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,'ebook',0,NULL,NULL,NULL,NULL,NULL,NULL,100.0,387328,NULL,NULL,NULL,NULL,NULL,-482028619515353839,1,NULL,5785377740721354521,NULL,0,NULL,NULL,772718400,2025,NULL,NULL,NULL,'Virgin',NULL,NULL,0,0,17551287442,NULL,602767352,NULL,1810905299,442404459,'','143509',14,1810905308,0,0,0,772702549,'productType=S&price=0&salableAdamId=1810905308&pricingParameters=HQRDL',128,NULL,NULL,'J19N_S_190099478929076',NULL,'Universal:isrc:NZUM72500022',NULL,NULL,'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/72/3c/07/723c07a7-4ff6-b052-927d-6997fff13676/25UMGIM60545.rgb.jpg/170x170bb.jpg',NULL,1751284926,'Shapeshifter',1966791522949379453,NULL,NULL);
INSERT INTO "download" VALUES (6936249076851270152,NULL,'Lorde',0,NULL,NULL,0,NULL,NULL,0,0,'https://p19-buy.itunes.apple.com/WebObjects/MZFastFinance.woa/wa/songDownloadDone?download-id=J19N_S_190099478929076&cancel=1','com.apple.iBooks','Lorde',1,11,'Virgin','Ella Marija Lani Yelich-O''Connor, James Harmon Stack & Andrew Aged',NULL,NULL,NULL,0,257066,2,0,NULL,3,0,0,0,0,0,'https://aod.itunes.apple.com/itunes-assets/HLSMusic221/v4/dd/ab/c4/ddabc4d6-35b8-1f0b-d558-b0c0493a2ed8/P1145527675_default.m3u8','Pop',3,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,'ebook',0,NULL,NULL,NULL,NULL,NULL,NULL,100.0,387328,NULL,NULL,NULL,NULL,NULL,-482028619515353839,1,NULL,5785377740721354521,NULL,0,NULL,NULL,772718400,2025,NULL,NULL,NULL,'Virgin',NULL,NULL,0,0,17551287442,NULL,602767352,NULL,1810905299,442404459,'','143509',14,1810905308,0,0,0,772702549,'productType=S&price=0&salableAdamId=1810905308&pricingParameters=HQRDL',128,NULL,NULL,'J19N_S_190099478929076',NULL,'Universal:isrc:NZUM72500022',NULL,NULL,'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/72/3c/07/723c07a7-4ff6-b052-927d-6997fff13676/25UMGIM60545.rgb.jpg/170x170bb.jpg',NULL,1751284926,'Shapeshifter',1966791522949379453,NULL,NULL);
INSERT INTO "download" VALUES (6936249076851270153,NULL,'Lorde',0,NULL,NULL,0,NULL,NULL,0,0,'https://p19-buy.itunes.apple.com/WebObjects/MZFastFinance.woa/wa/songDownloadDone?download-id=J19N_S_190099478929076&cancel=1','com.apple.iBooks','Lorde',1,11,'Virgin','Ella Marija Lani Yelich-O''Connor, James Harmon Stack & Andrew Aged',NULL,NULL,NULL,0,257066,2,0,NULL,3,0,0,0,0,0,'https://aod.itunes.apple.com/itunes-assets/HLSMusic221/v4/dd/ab/c4/ddabc4d6-35b8-1f0b-d558-b0c0493a2ed8/P1145527675_default.m3u8','Pop',3,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,'ebook',0,NULL,NULL,NULL,NULL,NULL,NULL,100.0,387328,NULL,NULL,NULL,NULL,NULL,-482028619515353839,1,NULL,5785377740721354521,NULL,0,NULL,NULL,772718400,2025,NULL,NULL,NULL,'Virgin',NULL,NULL,0,0,17551287442,NULL,602767352,NULL,1810905299,442404459,'','143509',14,1810905308,0,0,0,772702549,'productType=S&price=0&salableAdamId=1810905308&pricingParameters=HQRDL',128,NULL,NULL,'J19N_S_190099478929076',NULL,'Universal:isrc:NZUM72500022',NULL,NULL,'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/72/3c/07/723c07a7-4ff6-b052-927d-6997fff13676/25UMGIM60545.rgb.jpg/170x170bb.jpg',NULL,1751284926,'Shapeshifter',1966791522949379453,NULL,NULL);
INSERT INTO "download_policy" VALUES (-482028619515353839,X'62706c6973743030d4010203040506191a582476657273696f6e58246f626a65637473592461726368697665725424746f7012000186a0a5070811121355246e756c6cd4090a0b0c0d0e0f1057626167747970655572756c6573546b696e645624636c61737380038000800280045565626f6f6b5470726f64d2141516175824636c61737365735a24636c6173736e616d65a217185f10105353446f776e6c6f6164506f6c696379584e534f626a6563745f100f4e534b657965644172636869766572d11b1c54726f6f74800108111a232d32373d434c545a5f66686a6c6e74797e879295a8b1c3c6cb0000000000000101000000000000001d000000000000000000000000000000cd');
INSERT INTO "download_state" VALUES (1,6936249076851270150,'SSDownloadPhaseDownloading',0,0,0,1,1,1,0,-1,0,0,0,0,0,NULL,NULL);
INSERT INTO "persistent_manager" VALUES (-122653603835657826,'com.apple.Music',0,1,0,'com.apple.MediaPlayer.MPStoreDownloadManager');
INSERT INTO "persistent_manager" VALUES (3983691432232517437,'atc',1,1,0,'com.apple.atc');
INSERT INTO "persistent_manager_kind" VALUES (-5455443308017987184,3983691432232517437,'music-video');
INSERT INTO "persistent_manager_kind" VALUES (-4159605178976320956,-122653603835657826,'music-video');
INSERT INTO "persistent_manager_kind" VALUES (-3724789366776662195,3983691432232517437,'podcast');
INSERT INTO "persistent_manager_kind" VALUES (-2934406485076676697,-122653603835657826,'feature-movie');
INSERT INTO "persistent_manager_kind" VALUES (-1853578885913404635,-122653603835657826,'song');
INSERT INTO "persistent_manager_kind" VALUES (-485665347751747714,3983691432232517437,'ringtone');
INSERT INTO "persistent_manager_kind" VALUES (2327124089919026831,3983691432232517437,'song');
INSERT INTO "persistent_manager_kind" VALUES (3620912953913502965,3983691432232517437,'tone');
INSERT INTO "persistent_manager_kind" VALUES (3697265410986753061,3983691432232517437,'book');
INSERT INTO "persistent_manager_kind" VALUES (3765505936337730980,3983691432232517437,'tv-episode');
INSERT INTO "persistent_manager_kind" VALUES (3766453120645311522,-122653603835657826,'tv-episode');
INSERT INTO "persistent_manager_kind" VALUES (5278295194015425827,3983691432232517437,'feature-movie');
INSERT INTO "persistent_manager_kind" VALUES (7803262908021535763,3983691432232517437,'ebook');
INSERT INTO "persistent_manager_kind" VALUES (8234187785284895462,3983691432232517437,'videoPodcast');
INSERT INTO "purchase_manager" VALUES (1460693642792291151,'MusicPlayer','com.apple.Music.MPStoreDownloadManager','com.apple.Music','prod');
INSERT INTO "trnsaction" VALUES (1966791522949379453,NULL,0);
CREATE INDEX IF NOT EXISTS "application_workspace_state_bundle_id" ON "application_workspace_state" (
	"bundle_id"
);
CREATE INDEX IF NOT EXISTS "asset_download_id" ON "asset" (
	"download_id"
);
CREATE INDEX IF NOT EXISTS "download_is_restore" ON "download" (
	"is_restore"
);
CREATE INDEX IF NOT EXISTS "download_kind" ON "download" (
	"kind"
);
CREATE INDEX IF NOT EXISTS "download_priority_order_key" ON "download" (
	"priority"	DESC,
	"order_key"	ASC
);
CREATE INDEX IF NOT EXISTS "preorder_preorder_id" ON "preorder" (
	"store_preorder_id"
);
COMMIT;
