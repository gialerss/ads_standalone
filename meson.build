project(
  'TcAdsDll',
  'cpp',
  version: '0.1.0',
  default_options: [
    'buildtype=release',
    'warning_level=3',
    'cpp_std=c++14',
  ],
)

common_sources = files(
  'vendor/ADS/AdsLib/AdsDef.cpp',
  'vendor/ADS/AdsLib/AdsDevice.cpp',
  'vendor/ADS/AdsLib/AdsFile.cpp',
  'vendor/ADS/AdsLib/AdsLib.cpp',
  'vendor/ADS/AdsLib/MasterDcStatAccess.cpp',
  'vendor/ADS/AdsLib/ECatAccess.cpp',
  'vendor/ADS/AdsLib/Frame.cpp',
  'vendor/ADS/AdsLib/LicenseAccess.cpp',
  'vendor/ADS/AdsLib/Log.cpp',
  'vendor/ADS/AdsLib/RTimeAccess.cpp',
  'vendor/ADS/AdsLib/RegistryAccess.cpp',
  'vendor/ADS/AdsLib/RouterAccess.cpp',
  'vendor/ADS/AdsLib/Sockets.cpp',
  'vendor/ADS/AdsLib/SymbolAccess.cpp',
  'vendor/ADS/AdsLib/bhf/ParameterList.cpp',
)

router_sources = files(
  'vendor/ADS/AdsLib/standalone/AdsLib.cpp',
  'vendor/ADS/AdsLib/standalone/AmsConnection.cpp',
  'vendor/ADS/AdsLib/standalone/AmsNetId.cpp',
  'vendor/ADS/AdsLib/standalone/AmsPort.cpp',
  'vendor/ADS/AdsLib/standalone/AmsRouter.cpp',
  'vendor/ADS/AdsLib/standalone/NotificationDispatcher.cpp',
)

wrapper_sources = files('native/src/tcadsdll.cpp')

includes = include_directories(
  'vendor/ADS/AdsLib',
  'vendor/ADS/tools',
)

deps = [
  dependency('threads'),
  meson.get_compiler('cpp').find_library('ws2_32'),
]

rename_args = [
  '-DAdsPortCloseEx=StandaloneAdsPortCloseEx',
  '-DAdsPortOpenEx=StandaloneAdsPortOpenEx',
  '-DAdsGetLocalAddressEx=StandaloneAdsGetLocalAddressEx',
  '-DAdsSyncSetTimeoutEx=StandaloneAdsSyncSetTimeoutEx',
  '-DAdsSyncReadReqEx2=StandaloneAdsSyncReadReqEx2',
  '-DAdsSyncReadDeviceInfoReqEx=StandaloneAdsSyncReadDeviceInfoReqEx',
  '-DAdsSyncReadStateReqEx=StandaloneAdsSyncReadStateReqEx',
  '-DAdsSyncReadWriteReqEx2=StandaloneAdsSyncReadWriteReqEx2',
  '-DAdsSyncWriteReqEx=StandaloneAdsSyncWriteReqEx',
  '-DAdsSyncWriteControlReqEx=StandaloneAdsSyncWriteControlReqEx',
  '-DAdsSyncAddDeviceNotificationReqEx=StandaloneAdsSyncAddDeviceNotificationReqEx',
  '-DAdsSyncDelDeviceNotificationReqEx=StandaloneAdsSyncDelDeviceNotificationReqEx',
]

ads_core = static_library(
  'ads_core',
  [common_sources, router_sources],
  cpp_args: rename_args,
  include_directories: includes,
  dependencies: deps,
  pic: true,
)

shared_library(
  'TcAdsDll',
  wrapper_sources,
  link_with: ads_core,
  include_directories: includes,
  dependencies: deps,
  name_prefix: '',
  install: false,
)
