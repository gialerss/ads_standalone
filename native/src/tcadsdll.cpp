#define AdsPortCloseEx StandaloneAdsPortCloseEx
#define AdsPortOpenEx StandaloneAdsPortOpenEx
#define AdsGetLocalAddressEx StandaloneAdsGetLocalAddressEx
#define AdsSyncSetTimeoutEx StandaloneAdsSyncSetTimeoutEx
#define AdsSyncReadReqEx2 StandaloneAdsSyncReadReqEx2
#define AdsSyncReadDeviceInfoReqEx StandaloneAdsSyncReadDeviceInfoReqEx
#define AdsSyncReadStateReqEx StandaloneAdsSyncReadStateReqEx
#define AdsSyncReadWriteReqEx2 StandaloneAdsSyncReadWriteReqEx2
#define AdsSyncWriteReqEx StandaloneAdsSyncWriteReqEx
#define AdsSyncWriteControlReqEx StandaloneAdsSyncWriteControlReqEx
#define AdsSyncAddDeviceNotificationReqEx StandaloneAdsSyncAddDeviceNotificationReqEx
#define AdsSyncDelDeviceNotificationReqEx StandaloneAdsSyncDelDeviceNotificationReqEx
#include "AdsLib.h"

#undef AdsPortCloseEx
#undef AdsPortOpenEx
#undef AdsGetLocalAddressEx
#undef AdsSyncSetTimeoutEx
#undef AdsSyncReadReqEx2
#undef AdsSyncReadDeviceInfoReqEx
#undef AdsSyncReadStateReqEx
#undef AdsSyncReadWriteReqEx2
#undef AdsSyncWriteReqEx
#undef AdsSyncWriteControlReqEx
#undef AdsSyncAddDeviceNotificationReqEx
#undef AdsSyncDelDeviceNotificationReqEx

#if defined(_WIN32)
#define TCADS_EXPORT extern "C" __declspec(dllexport)
#else
#define TCADS_EXPORT extern "C"
#endif

TCADS_EXPORT long AdsPortCloseEx(long port)
{
    return StandaloneAdsPortCloseEx(port);
}

TCADS_EXPORT long AdsPortOpenEx()
{
    return StandaloneAdsPortOpenEx();
}

TCADS_EXPORT long AdsGetLocalAddressEx(long port, AmsAddr *pAddr)
{
    return StandaloneAdsGetLocalAddressEx(port, pAddr);
}

TCADS_EXPORT long AdsSyncSetTimeoutEx(long port, uint32_t timeout)
{
    return StandaloneAdsSyncSetTimeoutEx(port, timeout);
}

TCADS_EXPORT long AdsSyncReadReqEx2(long port, const AmsAddr *pAddr,
                                    uint32_t indexGroup, uint32_t indexOffset,
                                    uint32_t bufferLength, void *buffer,
                                    uint32_t *bytesRead)
{
    return StandaloneAdsSyncReadReqEx2(
        port, pAddr, indexGroup, indexOffset, bufferLength, buffer, bytesRead
    );
}

TCADS_EXPORT long AdsSyncReadDeviceInfoReqEx(long port, const AmsAddr *pAddr,
                                             char *devName, AdsVersion *version)
{
    return StandaloneAdsSyncReadDeviceInfoReqEx(port, pAddr, devName, version);
}

TCADS_EXPORT long AdsSyncReadStateReqEx(long port, const AmsAddr *pAddr,
                                        uint16_t *adsState, uint16_t *devState)
{
    return StandaloneAdsSyncReadStateReqEx(port, pAddr, adsState, devState);
}

TCADS_EXPORT long AdsSyncReadWriteReqEx2(long port, const AmsAddr *pAddr,
                                         uint32_t indexGroup,
                                         uint32_t indexOffset,
                                         uint32_t readLength, void *readData,
                                         uint32_t writeLength,
                                         const void *writeData,
                                         uint32_t *bytesRead)
{
    return StandaloneAdsSyncReadWriteReqEx2(
        port,
        pAddr,
        indexGroup,
        indexOffset,
        readLength,
        readData,
        writeLength,
        writeData,
        bytesRead
    );
}

TCADS_EXPORT long AdsSyncWriteReqEx(long port, const AmsAddr *pAddr,
                                    uint32_t indexGroup, uint32_t indexOffset,
                                    uint32_t bufferLength, const void *buffer)
{
    return StandaloneAdsSyncWriteReqEx(
        port, pAddr, indexGroup, indexOffset, bufferLength, buffer
    );
}

TCADS_EXPORT long AdsSyncWriteControlReqEx(long port, const AmsAddr *pAddr,
                                           uint16_t adsState,
                                           uint16_t devState,
                                           uint32_t bufferLength,
                                           const void *buffer)
{
    return StandaloneAdsSyncWriteControlReqEx(
        port, pAddr, adsState, devState, bufferLength, buffer
    );
}

TCADS_EXPORT long AdsSyncAddDeviceNotificationReqEx(
    long port, const AmsAddr *pAddr, uint32_t indexGroup, uint32_t indexOffset,
    const AdsNotificationAttrib *pAttrib, PAdsNotificationFuncEx pFunc,
    uint32_t hUser, uint32_t *pNotification)
{
    return StandaloneAdsSyncAddDeviceNotificationReqEx(
        port, pAddr, indexGroup, indexOffset, pAttrib, pFunc, hUser, pNotification
    );
}

TCADS_EXPORT long AdsSyncDelDeviceNotificationReqEx(
    long port, const AmsAddr *pAddr, uint32_t hNotification)
{
    return StandaloneAdsSyncDelDeviceNotificationReqEx(port, pAddr, hNotification);
}

TCADS_EXPORT long AdsAddRoute(AmsNetId ams, const char *ip)
{
    return bhf::ads::AddLocalRoute(ams, ip);
}

TCADS_EXPORT void AdsDelRoute(AmsNetId ams)
{
    bhf::ads::DelLocalRoute(ams);
}

TCADS_EXPORT void AdsSetLocalAddress(AmsNetId ams)
{
    bhf::ads::SetLocalAddress(ams);
}
