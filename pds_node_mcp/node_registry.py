"""Central registry of PDS discipline node HTTP-config.

Each entry is the minimum the 5 functional tools need: HTTP base URL,
data root, mission list, and whether the directory tree has a mission
layer. No prompt content (workflow notes / abbreviation tables) lives
here — agents must supply that in their own system prompt.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class NodeConfig:
    """Static HTTP configuration for one PDS discipline node."""

    node_id: str
    base_url: str
    display_name: str
    data_root: str
    has_mission_layer: bool
    missions: tuple[dict[str, str], ...] = field(default_factory=tuple)


_GEO_MISSIONS: tuple[dict[str, str], ...] = (
    {"name": 'm2020', "description": 'Mars 2020 / Perseverance (PIXL, SHERLOC, Mastcam-Z, SuperCam, RIMFAX)'},
    {"name": 'insight', "description": 'InSight lander (SEIS, HP3, RISE, IDA)'},
    {"name": 'msl', "description": 'Mars Science Laboratory / Curiosity (ChemCam, APXS, CheMin, SAM, Mastcam, MAHLI, DAN)'},
    {"name": 'mro', "description": 'Mars Reconnaissance Orbiter (HiRISE, CTX, CRISM, SHARAD, MCS)'},
    {"name": 'mer', "description": 'Mars Exploration Rovers — Spirit (MER2) and Opportunity (MER1) (Pancam, Mini-TES, APXS, MB, MI)'},
    {"name": 'mex', "description": 'Mars Express (HRSC, OMEGA, MARSIS, PFS, SPICAM, MaRS)'},
    {"name": 'ody', "description": 'Mars Odyssey (THEMIS, GRS, NS)'},
    {"name": 'phx', "description": 'Phoenix lander (TEGA, MECA, SSI, OM, RAC)'},
    {"name": 'mgs', "description": 'Mars Global Surveyor (MOC, MOLA, TES, MAG)'},
    {"name": 'mpf', "description": 'Mars Pathfinder (IMP, APXS)'},
    {"name": 'viking', "description": 'Viking (VL1, VL2, VO1, VO2 — camera, IRTM, MAWD)'},
    {"name": 'mariner', "description": 'Mariner missions'},
    {"name": 'mars', "description": 'Mars miscellaneous / Mars Express ancillary'},
    {"name": 'mgn', "description": 'Magellan (SAR, altimetry, radiometry, emissivity)'},
    {"name": 'premgn', "description": 'Pre-Magellan Venus data (Pioneer Venus Orbiter)'},
    {"name": 'venus', "description": 'Venus miscellaneous'},
    {"name": 'messenger', "description": 'MESSENGER at Mercury (MDIS, GRNS, XRS, MLA, MASCS)'},
    {"name": 'grail', "description": 'GRAIL lunar gravity (LGRS)'},
    {"name": 'clps', "description": 'Commercial Lunar Payload Services'},
    {"name": 'lunar', "description": 'Lunar missions (Clementine, Lunar Prospector, Chandrayaan, Kaguya, Apollo)'},
    {"name": 'lro', "description": 'Lunar Reconnaissance Orbiter (LOLA, Diviner, LROC, Mini-RF, LAMP)'},
    {"name": 'earth', "description": 'Earth-based observations'},
    {"name": 'lab', "description": 'Laboratory measurements'},
    {"name": 'near', "description": 'NEAR Shoemaker at Eros (NLR, MSI, XGRS, MAG)'},
)


_PPI_MISSIONS: tuple[dict[str, str], ...] = (
    {"name": 'cassini', "description": "Cassini at Saturn (CAPS, MAG, MIMI-CHEMS/INCA/LEMMS, RPWS, INMS). Also filter 'CO' for PDS3 IDs."},
    {"name": 'galileo', "description": "Galileo at Jupiter + flybys of Earth/Venus/asteroids (EPD, MAG, PLS, PWS, PPR, HIC, SSD, RSS). Also filter 'GO' for PDS3 IDs."},
    {"name": 'juno', "description": "Juno at Jupiter (Waves, JADE/JAD, JEDI/JED, FGM, ASC). Also filter 'JNO' for PDS3 IDs."},
    {"name": 'VG1', "description": "Voyager 1 at Jupiter, Saturn, and interplanetary (CRS, LECP, MAG, PLS, PWS, PRA, RSS). Also filter 'vg1' for PDS4."},
    {"name": 'VG2', "description": "Voyager 2 at Jupiter, Saturn, Uranus, Neptune, and interplanetary (CRS, LECP, MAG, PLS, PWS, PRA, RSS). Also filter 'vg2' for PDS4."},
    {"name": 'MESS', "description": "MESSENGER at Mercury (EPPS incl. FIPS & EPS, MAG). Also filter 'messenger' for PDS4 bundle. Target: Mercury."},
    {"name": 'MEX', "description": 'Mars Express (ASPERA-3 incl. ELS/IMA/NPI, MARSIS). Target: Mars.'},
    {"name": 'maven', "description": 'MAVEN at Mars (MAG, LPW, SEP, STATIC, SWEA, SWIA, EUV, ROSE). Target: Mars.'},
    {"name": 'P10', "description": "Pioneer 10 at Jupiter (CPI, CRT, GTT, HVM, PA, TRD, UV). Also filter 'p10' for PDS4."},
    {"name": 'P11', "description": "Pioneer 11 at Jupiter and Saturn (CPI, CRT, FGM, GTT, HVM, PA, TRD, UV). Also filter 'p11' for PDS4."},
    {"name": 'ULY', "description": "Ulysses at Jupiter and interplanetary (COSPIN, EPAC, HISCALE, SWOOPS, VHM-FGM, URAP, GAS, GRB, SCE, SWICS). Also filter 'ulysses' for PDS4."},
    {"name": 'NH', "description": 'New Horizons at Jupiter and Pluto (PEPSSI, SWAP). Target: Jupiter, Pluto.'},
    {"name": 'PVO', "description": "Pioneer Venus Orbiter (OEFD, OETP, OIMS, OMAG, ONMS, ORPA, ORSE). Also filter 'pvo' for PDS4. Target: Venus."},
    {"name": 'LP', "description": "Lunar Prospector (MAG, ER — electron reflectometer). Also filter 'lp' for PDS4. Target: Moon."},
    {"name": 'MGS', "description": "Mars Global Surveyor (MAG/ER, RSS). Also filter 'mgs' for PDS4. Target: Mars."},
    {"name": 'NEAR', "description": 'NEAR Shoemaker (MAG). Target: Eros, Earth flyby.'},
    {"name": 'M10', "description": 'Mariner 10 (MAG, PLS). Target: Mercury.'},
    {"name": 'LRO', "description": "Lunar Reconnaissance Orbiter (CRaTER). Also filter 'lro' for PDS4. Target: Moon."},
    {"name": 'ODY', "description": 'Mars Odyssey (MARIE — radiation). Target: Mars.'},
    {"name": 'MSL', "description": 'Mars Science Laboratory / Curiosity (RAD — radiation). Target: Mars.'},
    {"name": 'insight', "description": 'InSight (IFG — fluxgate magnetometer). Target: Mars.'},
    {"name": 'vex', "description": 'Venus Express (ASPERA-4 ELS, MAG). Target: Venus.'},
    {"name": 'ICE', "description": 'International Cometary Explorer (EPAS, MAG, PLAWAV, RADWAV, SWPLAS). Target: Giacobini-Zinner.'},
    {"name": 'GIO', "description": 'Giotto (IMS incl. HERS/HIS, JPA, MAG). Target: Halley.'},
    {"name": 'VEGA', "description": 'Vega 1 & 2 (MISCHA, PM1, TNM). Target: Halley.'},
    {"name": 'DS1', "description": 'Deep Space 1 (PEPE). Target: Borrelly.'},
    {"name": 'radiojove', "description": 'Radio JOVE ground-based radio observations of Jupiter.'},
)


_IMG_MISSIONS: tuple[dict[str, str], ...] = (
    {"name": 'cassini', "description": 'Cassini imaging at Saturn (ISS NAC/WAC). Nests into cassini_orbiter/, opus/, pds4/, public/.'},
    {"name": 'galileo', "description": 'Galileo SSI imaging at Jupiter and asteroid flybys (Gaspra, Ida).'},
    {"name": 'voyager', "description": 'Voyager 1 & 2 ISS imaging — Jupiter, Saturn, Uranus, Neptune.'},
    {"name": 'mariner6', "description": 'Mariner 6 Mars flyby imaging (1969).'},
    {"name": 'mariner7', "description": 'Mariner 7 Mars flyby imaging (1969).'},
    {"name": 'mariner9', "description": 'Mariner 9 Mars orbiter imaging (1971-72).'},
    {"name": 'mariner10', "description": 'Mariner 10 Mercury and Venus imaging (1973-75).'},
    {"name": 'viking_orbiter', "description": 'Viking Orbiter 1 & 2 imaging of Mars (1976-80).'},
    {"name": 'viking_lander', "description": 'Viking Lander 1 & 2 surface imaging at Mars.'},
    {"name": 'magellan', "description": 'Magellan SAR/altimetry/radiometry/emissivity imaging at Venus.'},
    {"name": 'messenger', "description": 'MESSENGER MDIS imaging at Mercury (legacy IMG mirror).'},
    {"name": 'near', "description": 'NEAR Shoemaker MSI imaging at asteroid Eros.'},
    {"name": 'stardust', "description": 'Stardust NAVCAM imaging of comet Wild 2 + Tempel 1 flyby.'},
    {"name": 'deepimpact', "description": 'Deep Impact HRI/MRI/ITS imaging at comet Tempel 1.'},
    {"name": 'mro', "description": 'Mars Reconnaissance Orbiter cameras at IMG: img/data/mro/ctx/ (CTX EDR, ~5500 mrox_* volumes), img/data/mro/hirise/ (HiRISE EXTRAS only — main RDR not mirrored at IMG, hosted at GEO), img/data/mro/marci/.'},
    {"name": 'mer', "description": 'Mars Exploration Rovers (Spirit=MER2, Opportunity=MER1) imaging: img/data/mer/ and direct PDS3 dirs img/data/mer1-* / mer2-* (Pancam, Navcam, Hazcam, Mini-TES, APXS).'},
    {"name": 'lro', "description": 'LRO LROC imaging (limited mirror) — full LROC archive is at the LROC node.'},
)


_RMS_MISSIONS: tuple[dict[str, str], ...] = (
    {"name": 'COISS', "description": 'Cassini ISS — Imaging Science Subsystem (NAC + WAC). Saturn rings, satellites, atmosphere.'},
    {"name": 'COUVIS', "description": 'Cassini UVIS — Ultraviolet Imaging Spectrograph. UV spectroscopy (SPEC), stellar/solar occultations (SSB), calibrated products (CALIB). Covers rings AND satellite surfaces (Rhea, Enceladus, etc.).'},
    {"name": 'COVIMS', "description": 'Cassini VIMS — Visual and Infrared Mapping Spectrometer. Rings + satellites.'},
    {"name": 'COCIRS', "description": 'Cassini CIRS — Composite InfraRed Spectrometer. Saturn/satellite atmospheres.'},
    {"name": 'CORSS', "description": 'Cassini Radio Science Subsystem ring/atmosphere occultations.'},
    {"name": 'COSP', "description": 'Cassini SPICE kernels (RMS mirror).'},
    {"name": 'VG_28xx', "description": 'Voyager 1/2 ring occultations (PPS/UVS/RSS).'},
    {"name": 'VG_2xxx', "description": 'Voyager 1/2 imaging (ISS) — Jupiter, Saturn, Uranus, Neptune.'},
    {"name": 'VGISS', "description": 'Voyager 1/2 ISS PDS4 calibrated/raw images.'},
    {"name": 'GO_00xx', "description": 'Galileo SSI imaging — Jupiter/satellites/ring system.'},
    {"name": 'EBROCC', "description": 'Earth-Based Ring Occultations (1989 Saturn, 1980s/90s Uranus).'},
    {"name": 'ESO_xxxx', "description": 'European Southern Observatory ground-based ring observations.'},
    {"name": 'RES_xxxx', "description": 'Reduced Earth-based stellar occultation results.'},
    {"name": 'HSTI', "description": 'Hubble WFPC2 imaging of rings/satellites.'},
    {"name": 'HSTJ', "description": 'Hubble ACS imaging of rings/satellites.'},
    {"name": 'HSTU', "description": 'Hubble WFC3/STIS imaging of rings/satellites.'},
    {"name": 'HSTN', "description": 'Hubble NICMOS imaging of rings/satellites.'},
    {"name": 'NHxxLO', "description": 'New Horizons LORRI imaging — Pluto, KBOs, ring search.'},
    {"name": 'NHxxMV', "description": 'New Horizons MVIC (Ralph) imaging.'},
    {"name": 'ASTROM', "description": 'Ground/HST astrometric measurements of irregular satellites.'},
    {"name": 'cassini_iss', "description": 'PDS4 bundle: Cassini ISS observations (cruise + Saturn tour).'},
    {"name": 'cassini_vims', "description": 'PDS4 bundle: Cassini VIMS observations.'},
    {"name": 'cassini_uvis', "description": 'PDS4 bundle: Cassini UVIS occultations.'},
)


_SBN_MISSIONS: tuple[dict[str, str], ...] = (
    {"name": 'dawn', "description": 'Dawn at Vesta + Ceres — pds3/dawn/{fc,grand,grav,vir}/. FC=Framing Camera, GRaND=Gamma Ray and Neutron Detector, GRAV=gravity, VIR=Visible+IR Mapping Spectrometer.'},
    {"name": 'near', "description": 'NEAR Shoemaker at asteroid Eros — pds3/near/<NEAR_A_*>/. Instruments: MSI (imaging), NLR (laser ranging), NIS (near-IR spectrometer), MAG, GRS, XRS.'},
    {"name": 'hayabusa', "description": 'Hayabusa at asteroid Itokawa — pds3/hayabusa/. Instruments: AMICA, NIRS, LIDAR, XRS.'},
    {"name": 'cassini', "description": 'Cassini small-body imaging (PSI mirror, distinct from RMS/PPI/ATM).'},
    {"name": 'galileo', "description": 'Galileo small-body imaging — Gaspra, Ida flybys (PSI mirror).'},
    {"name": 'ulysses', "description": 'Ulysses small-body observations (PSI mirror).'},
    {"name": 'iras', "description": 'IRAS infrared asteroid/comet observations.'},
    {"name": 'neat', "description": 'NEAT survey asteroid astrometry/photometry.'},
    {"name": 'msx', "description": 'MSX (Midcourse Space Experiment) asteroid IR observations.'},
    {"name": 'non_mission', "description": 'Ground/space-based non-mission small-body data archives.'},
    {"name": 'multi_mission', "description": 'Cross-mission small-body data products.'},
    {"name": 'orex', "description": 'OSIRIS-REx at asteroid Bennu — pds4/orex/{orex.ocams, orex.ovirs, orex.otes, orex.ola, orex.rexis, orex.spectral_analysis, ...}. Each is a PDS4 bundle with LID urn:nasa:pds:<bundle_name>.'},
    {"name": 'hayabusa2', "description": 'Hayabusa2 at asteroid Ryugu — pds4/hayabusa2/. Instruments: ONC, NIRS3, TIR, LIDAR, MASCOT.'},
    {"name": 'clipper', "description": 'Europa Clipper (PDS4-only at this archive).'},
    {"name": 'ldex', "description": 'LADEE dust experiment (PDS4 archive).'},
    {"name": 'ro-c', "description": "Rosetta at comet 67P — NOT hosted at PSI. Lives at UMD's pds-smallbodies.astro.umd.edu/holdings/. Out of reach from this base_url."},
    {"name": 'stardust', "description": 'Stardust at Wild 2 / Tempel 1 — NOT hosted at PSI (UMD-only). Out of reach.'},
    {"name": 'di', "description": 'Deep Impact at Tempel 1 — NOT hosted at PSI (UMD-only). Out of reach.'},
    {"name": 'lucy', "description": 'Lucy at Trojan asteroids — published at MIT/JPL mirrors (not yet at PSI). Out of reach from this base_url.'},
    {"name": 'dart', "description": 'DART impactor on Didymos/Dimorphos — published at JHUAPL mirror (not at PSI). Out of reach.'},
)


_ATM_MISSIONS: tuple[dict[str, str], ...] = (
    {"name": 'MROM', "description": 'Mars Reconnaissance Orbiter MCS (Mars Climate Sounder) — atmospheric temperature/aerosols.'},
    {"name": 'MAVENM', "description": 'MAVEN at Mars (NGIMS, IUVS, SWIA, SWEA, SEP) — upper atmosphere/ionosphere.'},
    {"name": 'MEXSPI', "description": 'Mars Express SPICAM — UV/IR atmospheric sensing.'},
    {"name": 'MEXASP', "description": 'Mars Express ASPERA-3 plasma/neutral atom (atmospheres mirror).'},
    {"name": 'MGSR', "description": 'Mars Global Surveyor radio science atmospheric occultations.'},
    {"name": 'PVO', "description": 'Pioneer Venus Orbiter (OETP, ONMS, OIR, OUVS) — Venus atmosphere/ionosphere.'},
    {"name": 'PVP', "description": 'Pioneer Venus Probes (Sounder, Day, Night, North, Bus).'},
    {"name": 'GP', "description": 'Galileo Probe — Jupiter atmospheric structure/composition (NMS, NEP, ASI, NFR).'},
    {"name": 'VG_IRIS', "description": 'Voyager IRIS thermal emission spectra (Jupiter, Saturn, Uranus, Neptune).'},
    {"name": 'VG_PRA', "description": 'Voyager Planetary Radio Astronomy (atmospheres mirror).'},
    {"name": 'HP', "description": 'Huygens Probe at Titan (DISR, HASI, GCMS, ACP, SSP, DWE).'},
    {"name": 'CO_HUYGENS', "description": 'Cassini-Huygens cruise atmospheric observations.'},
    {"name": 'cocirs', "description": 'Cassini CIRS — Composite InfraRed Spectrometer. Thermal emission spectra (10-600 cm⁻¹) of Saturn, Titan, and icy satellites (Enceladus, etc.). ATM mirror of RMS COCIRS volumes. ~84 volumes: cocirs_0401 … cocirs_1709.'},
    {"name": 'cors', "description": 'Cassini Radio Science (RSS) atmospheric/ionospheric occultations at Saturn, Titan, and icy satellites. ~430 volumes: cors_0001 … cors_0434.'},
    {"name": 'coiss', "description": 'Cassini ISS — Imaging Science Subsystem (ATM mirror). Limited holdings on ATM.'},
    {"name": 'coradr', "description": 'Cassini RADAR — Titan surface/atmosphere radiometry (ATM mirror). Limited holdings on ATM.'},
    {"name": 'MSL_REMS', "description": 'Mars Science Laboratory REMS — rover meteorology (pressure, temp, UV, RH, wind).'},
    {"name": 'M2020_MEDA', "description": 'Mars 2020 MEDA — rover meteorology (radiation, dust, temp, pressure, wind).'},
    {"name": 'PHX', "description": 'Phoenix lander — TEGA, MECA, atmospheric optical depth.'},
    {"name": 'EARTH_', "description": 'Earth-based atmospheric / supporting observations.'},
)


_NAIF_MISSIONS: tuple[dict[str, str], ...] = (
    {"name": 'lro-l-spice-6', "description": 'Lunar Reconnaissance Orbiter SPICE kernels.'},
    {"name": 'msl-m-spice-6', "description": 'Mars Science Laboratory / Curiosity SPICE kernels.'},
    {"name": 'mars2020-m-spice-6', "description": 'Mars 2020 / Perseverance SPICE kernels.'},
    {"name": 'insight-m-spice-6', "description": 'InSight lander SPICE kernels.'},
    {"name": 'mer1-m-spice-6', "description": 'Mars Exploration Rover Opportunity (MER-1) SPICE kernels.'},
    {"name": 'mer2-m-spice-6', "description": 'Mars Exploration Rover Spirit (MER-2) SPICE kernels.'},
    {"name": 'mex-e_m-spice-6', "description": 'Mars Express SPICE kernels.'},
    {"name": 'mro-m-spice-6', "description": 'Mars Reconnaissance Orbiter SPICE kernels.'},
    {"name": 'mgs-m-spice-6', "description": 'Mars Global Surveyor SPICE kernels.'},
    {"name": 'ody-m-spice-6', "description": 'Mars Odyssey SPICE kernels.'},
    {"name": 'maven-m-spice-6', "description": 'MAVEN SPICE kernels.'},
    {"name": 'co-s_e_v-spice-6', "description": 'Cassini-Huygens SPICE kernels (Saturn tour + cruise).'},
    {"name": 'vg1-j_s-spice-6', "description": 'Voyager 1 SPICE kernels (Jupiter, Saturn).'},
    {"name": 'vg2-j_s_u_n-spice-6', "description": 'Voyager 2 SPICE kernels (Jupiter, Saturn, Uranus, Neptune).'},
    {"name": 'go-j_e_a-spice-6', "description": 'Galileo SPICE kernels (Jupiter, Earth, asteroids).'},
    {"name": 'near-a-spice-6', "description": 'NEAR Shoemaker SPICE kernels.'},
    {"name": 'mess-e_v_h-spice-6', "description": 'MESSENGER SPICE kernels (Mercury cruise + orbit).'},
    {"name": 'juno-j-spice-6', "description": 'Juno SPICE kernels at Jupiter.'},
    {"name": 'nh-j_p_ss-spice-6', "description": 'New Horizons SPICE kernels (Jupiter, Pluto, KBO encounters).'},
    {"name": 'ro-c_e_a-spice-6', "description": 'Rosetta SPICE kernels (comet 67P, Earth flybys, asteroid flybys).'},
    {"name": 'orex-bennu-spice-6', "description": 'OSIRIS-REx SPICE kernels at asteroid Bennu.'},
    {"name": 'hyb2-ryugu-spice-6', "description": 'Hayabusa2 SPICE kernels at asteroid Ryugu.'},
    {"name": 'lucy-spice-6', "description": 'Lucy SPICE kernels (Trojan asteroid mission).'},
    {"name": 'dart-spice-6', "description": 'DART SPICE kernels (Didymos/Dimorphos impact).'},
)


NODE_REGISTRY: dict[str, NodeConfig] = {
    "geo": NodeConfig(
        node_id='geo',
        base_url='https://pds-geosciences.wustl.edu/',
        display_name='Geosciences (GEO)',
        data_root='',
        has_mission_layer=True,
        missions=_GEO_MISSIONS,
    ),
    "ppi": NodeConfig(
        node_id='ppi',
        base_url='https://pds-ppi.igpp.ucla.edu/',
        display_name='Planetary Plasma Interactions (PPI)',
        data_root='data/',
        has_mission_layer=False,
        missions=_PPI_MISSIONS,
    ),
    "lroc": NodeConfig(
        node_id='lroc',
        base_url='https://pds.lroc.im-ldi.com/',
        display_name='Lunar Reconnaissance Orbiter Camera (LROC)',
        data_root='data/',
        has_mission_layer=False,
    ),
    "img": NodeConfig(
        node_id='img',
        base_url='https://planetarydata.jpl.nasa.gov/',
        display_name='JPL Imaging Node (IMG)',
        data_root='img/data/',
        has_mission_layer=True,
        missions=_IMG_MISSIONS,
    ),
    "rms": NodeConfig(
        node_id='rms',
        base_url='https://pds-rings.seti.org/',
        display_name='Ring-Moon Systems (RMS)',
        data_root='holdings/volumes/',
        has_mission_layer=False,
        missions=_RMS_MISSIONS,
    ),
    "sbn": NodeConfig(
        node_id='sbn',
        base_url='https://sbnarchive.psi.edu/',
        display_name='Small Bodies Node (SBN — PSI mirror)',
        data_root='pds3/',
        has_mission_layer=True,
        missions=_SBN_MISSIONS,
    ),
    "atm": NodeConfig(
        node_id='atm',
        base_url='https://pds-atmospheres.nmsu.edu/',
        display_name='Atmospheres (ATM)',
        data_root='PDS/data/',
        has_mission_layer=False,
        missions=_ATM_MISSIONS,
    ),
    "naif": NodeConfig(
        node_id='naif',
        base_url='https://naif.jpl.nasa.gov/',
        display_name='Navigation and Ancillary Information Facility (NAIF)',
        data_root='pub/naif/pds/data/',
        has_mission_layer=True,
        missions=_NAIF_MISSIONS,
    ),
}


SUPPORTED_NODES = tuple(NODE_REGISTRY.keys())


def get_node_config(node_id: str) -> NodeConfig:
    """Look up a node by ID. Raises ValueError if unknown."""
    config = NODE_REGISTRY.get(node_id.lower())
    if config is None:
        raise ValueError(
            f"Unknown PDS node: {node_id!r}. "
            f"Supported nodes: {', '.join(SUPPORTED_NODES)}"
        )
    return config


def get_base_url(node_id: str) -> str:
    """Shortcut: get the base URL for a node."""
    return get_node_config(node_id).base_url
