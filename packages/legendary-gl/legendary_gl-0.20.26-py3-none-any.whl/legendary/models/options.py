# coding: utf-8

from argparse import Namespace
from asyncio import Queue as AIOQueue
from dataclasses import dataclass
from multiprocessing import Queue as MPQueue
from typing import Optional

from .manifest import Manifest
from .game import Game


@dataclass
class DownloaderManagerOptions:
    download_dir: str
    base_url: str
    cache_dir: Optional[str] = None
    resume_file: Optional[str] = None
    # queue options
    status_queue: Optional[MPQueue, AIOQueue] = None
    update_interval: float = 1.0
    # downloader options
    dl_timeout: float = 10.0
    max_workers: Optional[int] = None
    max_shared_memory: int = 1024 * 1024 * 1024


@dataclass
class DownloaderAnalysisOptions:
    manifest: Manifest
    old_manifest: Optional[Manifest] = None

    # additional features
    enable_patching: bool = True
    enable_resume: bool = True
    enable_process_opts: bool = False

    # filters
    prefix_include_filters: Optional[list] = None
    prefix_exclude_filters: Optional[list] = None
    suffix_include_filters: Optional[list] = None
    suffix_exclude_filters: Optional[list] = None
    install_tags: Optional[list] = None


@dataclass
class CorePrepareDownloadOpts:
    game: Game
    base_game: Game = None
    base_path: Optional[str] = None
    game_folder: Optional[str] = None

    # behavioural options
    force: bool = False
    repair: bool = False
    disable_delta: bool = False
    disable_https: bool = False
    repair_use_latest: bool = False

    # manifest options
    override_manifest: Optional[str] = None
    override_old_manifest: Optional[str] = None
    override_delta_manifest: Optional[str] = None
    override_base_url: Optional[str] = None
    override_platform: Optional[str] = None

    # downloader options
    preferred_cdn: Optional[str] = None
    disable_patching: bool = False
    disable_process_opts: bool = False
    status_queue: Optional[MPQueue, AIOQueue] = None
    max_shared_memory: Optional[int] = None
    max_workers: Optional[int] = None
    dl_timeout: Optional[float] = None
    # filtering
    prefix_include_filters: Optional[list] = None
    prefix_exclude_filters: Optional[list] = None
    suffix_include_filters: Optional[list] = None
    suffix_exclude_filters: Optional[list] = None


@dataclass
class CLIArgs(Namespace):
    # Commands
    full_help: bool = False
    version: bool = False
    subparser_name: str = ''

    # Global options
    yes: bool = False
    debug: bool = False
    pretty_json: bool = False
    api_timeout: float = 10.0
    config_file: str = ''

    # Shared options
    app_name: str = ''
    platform: str = ''
    json: bool = False
    ## list apps/files/installed
    csv: bool = False
    tsv: bool = False
    ## install / import
    with_dlcs: bool = False
    skip_dlcs: bool = False
    ## launch / cx config
    crossover_app: str = ''
    crossover_bottle: str = ''
    ## launch / status / info
    offline: bool = False
    ## launch / activate
    origin: bool = False
    ## alias / overlay
    action: str = ''

    # Activate parser
    uplay: bool = False

    # Alias parser
    app_or_alias: str = ''
    alias: str = ''

    # Auth parser
    auth_code: str = ''
    session_id: str = ''
    auth_delete: bool = False
    import_egs_auth: bool = False
    no_webview: bool = False

    # Cleanup parser
    keep_manifests: bool = False

    # CX parser
    reset: bool = False
    download: bool = False
    disable_version_check: False = False

    # EGL sync parser
    egl_manifest_path: str = ''
    egl_wine_prefix: str = ''
    enable_sync: bool = False
    disable_sync: bool = False
    one_shot: bool = False
    import_only: bool = False
    export_only: bool = False
    migrate: bool = False
    unlink: bool = False

    # EOS overlay parser
    path = None
    prefix = None
    app = None
    bottle = None

    # Import parser
    disable_check = None
    app_path: str = ''

    # Info parser
    app_name_or_manifest: str = ''

    # Install parser
    base_path = None
    game_folder = None
    shared_memory = None
    max_workers = None
    override_manifest = None
    override_old_manifest = None
    override_delta_manifest = None
    override_base_url = None
    force = None
    disable_patching = None
    no_install = None
    update_only = None
    dlm_debug = None
    file_prefix = None
    file_exclude_prefix = None
    install_tag = None
    order_opt = None
    dl_timeout = None
    save_path = None
    repair_mode = None
    repair_and_update = None
    ignore_space = None
    disable_delta = None
    reset_sdl = None
    skip_sdl = None
    disable_sdl = None
    preferred_cdn = None
    disable_https = None

    # Launch parser
    skip_version_check = None
    user_name_override = None
    dry_run = None
    language = None
    wrapper = None
    set_defaults = None
    reset_defaults = None
    executable_override = None
    wine_bin = None
    wine_pfx = None
    no_wine = None
    crossover = None

    # List parser
    include_ue = None
    include_noasset = None
    force_refresh = None

    # List installed parser
    check_updates = None
    include_dir = None

    # List files parser
    force_download = None
    hashlist = None

    # Move parser
    new_path: str = ''
    skip_move = None

    # Sync saves parser
    download_only = None
    upload_only = None
    force_upload = None
    disable_filters = None
    delete_incomplete = None

    # Token parse (hidden)
    bearer = None

    # Uninstall parser
    keep_files = None

