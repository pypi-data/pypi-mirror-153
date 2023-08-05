def get_ppa_published_binaries(launchpad, lp_arch_series, ppa):
    ppa_owner, ppa_name = ppa.split("/")
    archive = launchpad.people[ppa_owner].getPPAByName(name=ppa_name)
    # using pocket "Release" when using a PPA ...'
    pocket = "Release"
    sources = archive.getPublishedBinaries(
        exact_match=True,
        pocket=pocket,
        distro_arch_series=lp_arch_series,
        status="Published",
        ordered=True,
    )
    return sources


def get_ppa_sources(launchpad, lp_series, ppa):
    ppa_owner, ppa_name = ppa.split("/")
    archive = launchpad.people[ppa_owner].getPPAByName(name=ppa_name)
    # using pocket "Release" when using a PPA ...'
    pocket = "Release"
    sources = archive.getPublishedSources(
        exact_match=True,
        pocket=pocket,
        distro_series=lp_series,
        status="Published",
    )
    return sources
