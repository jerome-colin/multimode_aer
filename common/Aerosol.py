import xarray as xr

class Aerosol:
    # TODO: move to another dedicated file
    def __init__(self):
        self.species = ["DUST", "BLACK CARBON", "ORGANIC MATTER", "SEA SALT", "SULFATE", "NITRATE", "AMMONIUM"]
        self.species_short = ["DU", "BC", "OM", "SS", "SU", "NI", "AM"]
        self.relative_humidity = [.30, 0.50, 0.70, 0.80, 0.85, 0.90, 0.95]

        # Modal radius, CAMS, from Bastien
        _modal_radius = [[0.29, 0.29, 0.29, 0.29, 0.29, 0.29, 0.29],
                         [0.0118, 0.0118, 0.0118, 0.0118, 0.0118, 0.0118, 0.0118],
                         [0.024, 0.026, 0.028, 0.030, 0.032, 0.034, 0.039],
                         [0.1002, 0.1558, 0.1803, 0.19921, 0.2135, 0.2366, 0.2882],
                         [0.0212, 0.0259, 0.0289, 0.0315, 0.0335, 0.0367, 0.0442],
                         [0.035, 0.042, 0.0455, 0.04725, 0.0525, 0.0595, 0.0735],
                         [0.035, 0.043, 0.048, 0.052, 0.055, 0.061, 0.073]]
        self.modal_radius = xr.DataArray(_modal_radius, dims=("species", "rh"), coords={"species": self.species_short,
                                                                             "rh": self.relative_humidity})
        # Standard deviation on modal radius, CAMS, from Bastien
        _stddev = [[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
                   [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
                   [0.349, 0.349, 0.349, 0.349, 0.349, 0.349, 0.349],
                   [0.279, 0.279, 0.279, 0.279, 0.279, 0.279, 0.279],
                   [0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35],
                   [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
                   [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]]
        self.stddev = xr.DataArray(_stddev, dims=("species", "rh"), coords={"species": self.species_short,
                                                                             "rh": self.relative_humidity})
        # Refractive indexes
        # Warning: wavelength dimension not ordered, but follows S2A + REF (550nm), S2B diff neglected as a first approximation
        self.sentinel2_wavelengths = [0.443 , 0.492, 0.560, 0.664, 0.704, 0.740, 0.783, 0.830, 0.865, 0.945, 1.373, 1.613, 2.198]

        _s2_refractive_indexes_img_simu = [[[-0.007581,-0.005964,-0.005095,-0.003996,-0.004027,-0.004129,-0.004252,-0.004300,-0.004300,-0.004403,-0.004500,-0.004500,-0.004500],
                                     [-0.007581,-0.005964,-0.005095,-0.003996,-0.004027,-0.004129,-0.004252,-0.004300,-0.004300,-0.004403,-0.004500,-0.004500,-0.004500],
                                     [-0.007581,-0.005964,-0.005095,-0.003996,-0.004027,-0.004129,-0.004252,-0.004300,-0.004300,-0.004403,-0.004500,-0.004500,-0.004500],
                                     [-0.007581,-0.005964,-0.005095,-0.003996,-0.004027,-0.004129,-0.004252,-0.004300,-0.004300,-0.004403,-0.004500,-0.004500,-0.004500],
                                     [-0.007581,-0.005964,-0.005095,-0.003996,-0.004027,-0.004129,-0.004252,-0.004300,-0.004300,-0.004403,-0.004500,-0.004500,-0.004500],
                                     [-0.007581,-0.005964,-0.005095,-0.003996,-0.004027,-0.004129,-0.004252,-0.004300,-0.004300,-0.004403,-0.004500,-0.004500,-0.004500],
                                     [-0.007581,-0.005964,-0.005095,-0.003996,-0.004027,-0.004129,-0.004252,-0.004300,-0.004300,-0.004403,-0.004500,-0.004500,-0.004500]
                                         ],
                               [[-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10],
                                [-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10],
                                [-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10],
                                [-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10],
                                [-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10],
                                [-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10],
                                [-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10]
                                ],
                               [[-0.006000,-0.005959,-0.006293,-0.006682,-0.006704,-0.007172,-0.007732,-0.008356,-0.008826,-0.009804,-0.012830,-0.012749,-0.008574],
                                [-0.004724,-0.004690,-0.004930,-0.005215,-0.005229,-0.005575,-0.005989,-0.006452,-0.006801,-0.007526,-0.009793,-0.009749,-0.006869],
                                [-0.003679,-0.003653,-0.003840,-0.004061,-0.004072,-0.004342,-0.004664,-0.005025,-0.005297,-0.005862,-0.007642,-0.007615,-0.005534],
                                [-0.002978, -0.002956, -0.003108, -0.003286, -0.003296, -0.003514, -0.003775, -0.004066, -0.004286, -0.004744, -0.006197, -0.006181, -0.004637],
                                [-0.002444, -0.002427, -0.002556, -0.002707, -0.002715, -0.002899, -0.003118, -0.003363,
                                 -0.003548, -0.003933, -0.005162, -0.005152, -0.003966],
                                [-0.002029, -0.002014, -0.002118, -0.002240, -0.002245, -0.002394, -0.002572, -0.002771,
                                 -0.002921, -0.003233, -0.004242, -0.004242, -0.003424],
                                [-0.001348, -0.001339, -0.001407, -0.001488, -0.001492, -0.001591, -0.001709, -0.001841,
                                 -0.001941, -0.002149, -0.002840, -0.002851, -0.002553]
                                ],
                               [[-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000001,-0.000008,-0.000016,-0.000053,-0.000274,-0.000418,-0.001808],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000004,-0.000007,-0.000024,-0.000151,-0.000260,-0.001554],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000003,-0.000005,-0.000018,-0.000122,-0.000223,-0.001494],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000002,-0.000004,-0.000014,-0.000105,-0.000201,-0.001459],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000002,-0.000003,-0.000011,-0.000094,-0.000187,-0.001437],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000009,-0.000084,-0.000174,-0.001416],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000006,-0.000070,-0.000156,-0.001388]
                                ],
                               [[-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000059,-0.000156,-0.001693],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000063,-0.000128,-0.001018],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000063,-0.000123,-0.000880],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000064,-0.000120,-0.000811],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000064,-0.000115,-0.000693],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000001,-0.000002,-0.000065,-0.000110,-0.000575],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000001,-0.000003,-0.000066,-0.000105,-0.000456]
                                ],
                               [[-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000181],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000589],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000606],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000658],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000693],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000736]
                                ],
                               [[-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000059,-0.000156,-0.002579],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000063,-0.000128,-0.001838],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000063,-0.000123,-0.001686],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000064,-0.000120,-0.001610],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000002,-0.000064,-0.000115,-0.001481],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000001,-0.000002,-0.000065,-0.000110,-0.001351],
                                [-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000000,-0.000001,-0.000001,-0.000003,-0.000066,-0.000105,-0.001221]
                                ]]

        _s2_refractive_indexes_real_simu = [[[1.5300,1.5300,1.5300,1.5300,1.5274,1.5246,1.5213,1.5200,1.5200,1.5177,1.4338,1.3752,1.2283],
                                          [1.5300,1.5300,1.5300,1.5300,1.5274,1.5246,1.5213,1.5200,1.5200,1.5177,1.4338,1.3752,1.2283],
                                          [1.5300,1.5300,1.5300,1.5300,1.5274,1.5246,1.5213,1.5200,1.5200,1.5177,1.4338,1.3752,1.2283],
                                          [1.5300,1.5300,1.5300,1.5300,1.5274,1.5246,1.5213,1.5200,1.5200,1.5177,1.4338,1.3752,1.2283],
                                          [1.5300,1.5300,1.5300,1.5300,1.5274,1.5246,1.5213,1.5200,1.5200,1.5177,1.4338,1.3752,1.2283],
                                          [1.5300,1.5300,1.5300,1.5300,1.5274,1.5246,1.5213,1.5200,1.5200,1.5177,1.4338,1.3752,1.2283],
                                          [1.5300,1.5300,1.5300,1.5300,1.5274,1.5246,1.5213,1.5200,1.5200,1.5177,1.4338,1.3752,1.2283]
                                          ],
                                         [[1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75],
                                          [1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75],
                                          [1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75],
                                          [1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75],
                                          [1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75],
                                          [1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75],
                                          [1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75,1.75]
                                          ],
                                         [[1.4793,1.4787,1.4780,1.4774,1.4774,1.4774,1.4724,1.4699,1.4699,1.4697,1.4611,1.4472,1.3884],
                                          [1.4426,1.4416,1.4405,1.4395,1.4395,1.4395,1.4356,1.4336,1.4336,1.4332,1.4253,1.4138,1.3627],
                                          [1.4192,1.4181,1.4167,1.4159,1.4159,1.4151,1.4123,1.4107,1.4103,1.4096,1.4027,1.3929,1.3464],
                                          [1.4037,1.4026,1.4013,1.3995,1.3995,1.3995,1.3969,1.3952,1.3949,1.3941,1.3872,1.3783,1.3355],
                                          [1.3933,1.3918,1.3904,1.3886,1.3885,1.3882,1.3858,1.3843,1.3840,1.3834,1.3767,1.3684,1.3279],
                                          [1.3829,1.3811,1.3796,1.3778,1.3777,1.3770,1.3748,1.3735,1.3732,1.3728,1.3664,1.3588,1.3205],
                                          [1.3675,1.3655,1.3640,1.3622,1.3622,1.3614,1.3599,1.3590,1.3586,1.3578,1.3513,1.3450,1.3095]
                                          ],
                                         [[1.4258,1.4251,1.4231,1.4174,1.4157,1.4140,1.4118,1.4110,1.4110,1.4076,1.3991,1.3922,1.3722],
                                          [1.3763,1.3752,1.3726,1.3690,1.3680,1.3668,1.3655,1.3650,1.3650,1.3628,1.3553,1.3501,1.3256],
                                          [1.3651,1.3633,1.3607,1.3580,1.3572,1.3564,1.3554,1.3547,1.3544,1.3525,1.3453,1.3401,1.3142],
                                          [1.3581,1.3563,1.3537,1.3510,1.3502,1.3494,1.3484,1.3477,1.3474,1.3460,1.3394,1.3345,1.3074],
                                          [1.3537,1.3518,1.3492,1.3470,1.3462,1.3454,1.3444,1.3437,1.3434,1.3423,1.3355,1.3308,1.3037],
                                          [1.4261,1.4261,1.4261,1.4261,1.4261,1.4261,1.4261,1.4261,1.4261,1.4261,1.4261,1.4261,1.4261],
                                          [1.3443,1.3423,1.3398,1.3380,1.3372,1.3364,1.3354,1.3347,1.3344,1.3335,1.3270,1.3230,1.2946]
                                          ],
                                         [[1.5375,1.5343,1.5300,1.5249,1.5233,1.5220,1.5203,1.5186,1.5173,1.5143,1.4983,1.4893,1.4631],
                                          [1.4363,1.4340,1.4310,1.4274,1.4263,1.4254,1.4242,1.4230,1.4222,1.4202,1.4090,1.4021,1.3768],
                                          [1.4156,1.4135,1.4108,1.4075,1.4065,1.4056,1.4046,1.4035,1.4027,1.4010,1.3907,1.3843,1.3592],
                                          [1.4053,1.4033,1.4007,1.3975,1.3966,1.3957,1.3948,1.3937,1.3930,1.3914,1.3816,1.3754,1.3504],
                                          [1.3875,1.3857,1.3833,1.3804,1.3796,1.3788,1.3779,1.3770,1.3764,1.3749,1.3660,1.3602,1.3353],
                                          [1.3698,1.3681,1.3660,1.3633,1.3626,1.3619,1.3611,1.3603,1.3597,1.3584,1.3503,1.3449,1.3202],
                                          [1.3520,1.3506,1.3486,1.3463,1.3456,1.3450,1.3442,1.3435,1.3430,1.3419,1.3347,1.3296,1.3051]],
                                         [[1.6110,1.6110,1.6110,1.6110,1.6110,1.6110,1.6110,1.6110,1.6110,1.6110,1.6110,1.6110,1.6110],
                                          [1.4959,1.4951,1.4939,1.4930,1.4927,1.4925,1.4921,1.4920,1.4920,1.4914,1.4887,1.4868,1.4794],
                                          [1.4619,1.4611,1.4598,1.4580,1.4577,1.4575,1.4571,1.4570,1.4570,1.4564,1.4532,1.4507,1.4407],
                                          [1.4484,1.4473,1.4459,1.4450,1.4447,1.4445,1.4441,1.4438,1.4434,1.4426,1.4389,1.4359,1.4257],
                                          [1.4183,1.4171,1.4149,1.4140,1.4137,1.4135,1.4131,1.4128,1.4124,1.4116,1.4069,1.4038,1.3910],
                                          [1.3933,1.3913,1.3898,1.3880,1.3875,1.3869,1.3863,1.3860,1.3860,1.3853,1.3798,1.3766,1.3622],
                                          [1.3669,1.3653,1.3628,1.3610,1.3605,1.3599,1.3593,1.3590,1.3590,1.3583,1.3523,1.3484,1.3325]
                                          ],
                                         [[1.5375,1.5343,1.5300,1.5249,1.5233,1.5220,1.5203,1.5186,1.5173,1.5143,1.4983,1.4893,1.4728],
                                          [1.4363,1.4340,1.4310,1.4274,1.4263,1.4254,1.4242,1.4230,1.4222,1.4202,1.4090,1.4021,1.3835],
                                          [1.4156,1.4135,1.4108,1.4075,1.4065,1.4056,1.4046,1.4035,1.4027,1.4010,1.3907,1.3843,1.3653],
                                          [1.4053,1.4033,1.4007,1.3975,1.3966,1.3957,1.3948,1.3937,1.3930,1.3914,1.3816,1.3754,1.3562],
                                          [1.3875,1.3857,1.3833,1.3804,1.3796,1.3788,1.3779,1.3770,1.3764,1.3749,1.3660,1.3602,1.3405],
                                          [1.3698,1.3681,1.3660,1.3633,1.3626,1.3619,1.3611,1.3603,1.3597,1.3584,1.3503,1.3449,1.3249],
                                          [1.3520,1.3506,1.3486,1.3463,1.3456,1.3450,1.3442,1.3435,1.3430,1.3419,1.3347,1.3296,1.3092]
                                          ]]


        self.s2_refractive_indexes_real_simu = xr.DataArray(_s2_refractive_indexes_real_simu,
                                                        dims=("species", "rh", "wavelength"),
                                                        coords={"species": self.species_short,
                                                                "rh": self.relative_humidity,
                                                                "wavelength": self.sentinel2_wavelengths})

        self.s2_refractive_indexes_img_simu = xr.DataArray(_s2_refractive_indexes_img_simu,
                                               dims=("species", "rh", "wavelength"),
                                               coords={"species": self.species_short,
                                                       "rh": self.relative_humidity,
                                                       "wavelength": self.sentinel2_wavelengths})

        #TODO: create method get_refractive_indexes_reference with a linear interpolation of s2 values at 'ref'

    def get_properties(self, mode_nb, wavelength_simu, wavelength_ref, proportion, species, rh):
        aer_modal_radius = self.modal_radius.sel(species=species, rh=rh)
        aer_stddev = self.stddev.sel(species=species, rh=rh)
        aer_refractive_index_real_simu = self.s2_refractive_indexes_real_simu.sel(species=species, rh=rh, wavelength=wavelength_simu)
        aer_refractive_index_img_simu = self.s2_refractive_indexes_img_simu.sel(species=species, rh=rh, wavelength=wavelength_simu)

        tmp_refractive_index_real_ref_allwl = self.s2_refractive_indexes_real_simu.sel(species=species, rh=rh)
        #print(tmp_refractive_index_real_ref_allwl)
        aer_refractive_index_real_ref = tmp_refractive_index_real_ref_allwl.interp(wavelength=wavelength_ref)

        tmp_refractive_index_img_ref_allwl = self.s2_refractive_indexes_img_simu.sel(species=species, rh=rh)
        aer_refractive_index_img_ref = tmp_refractive_index_img_ref_allwl.interp(wavelength=wavelength_ref)

        #return aer_modal_radius, aer_stddev, aer_refractive_index_real_simu, aer_refractive_index_img_simu, aer_refractive_index_real_ref, aer_refractive_index_img_ref
        return self.as_str(mode_nb, species, proportion, aer_modal_radius, aer_stddev, aer_refractive_index_real_simu, aer_refractive_index_img_simu, aer_refractive_index_real_ref, aer_refractive_index_img_ref)

    def as_str(self, mode_nb, species, proportion, modal_radius, stddev, refractive_index_wa_simu_real, refractive_index_wa_simu_img, refractive_index_wa_ref_real, refractive_index_wa_ref_img, size_distribution_mode="LND"):
        aer_str = "SIZE DISTRIBUTION MODE %i (%s): %s\n" % (mode_nb+1, species, size_distribution_mode)
        aer_str += "    MODAL RADIUS (microns)  : %6.4f\n" % modal_radius
        aer_str += "    STANDARD DEVIATION (microns): %6.4f\n" % stddev
        aer_str += "    REFRACTIVE INDEX at WA_SIMU - Real part: %6.4f\n" % refractive_index_wa_simu_real
        aer_str += "    REFRACTIVE INDEX at WA_SIMU - Imaginary part (<0): %6.4f\n" % refractive_index_wa_simu_img
        aer_str += "    REFRACTIVE INDEX at WA_REF - Real part: %6.4f\n" % refractive_index_wa_ref_real
        aer_str += "    REFRACTIVE INDEX at WA_REF - Imaginary part (<0): %6.4f\n" % refractive_index_wa_ref_img
        aer_str += "    PROPORTION TO THE TOTAL AOT at WA_REF : %6.4f\n" % proportion

        return aer_str


class Model:

    def __init__(self, ratio_list, rh, wavelength_simu, wavelength_ref):
        self._nb_modes = 0

        self.species_short = ["DU", "BC", "OM", "SS", "SU", "NI", "AM"]
        self.ratio_list = ratio_list
        self.rh = rh
        self.wavelength_simu = wavelength_simu

        self.library = Aerosol()

        for i in range(len(self.ratio_list)):
            if self.ratio_list[i] != 0:
                self._nb_modes += 1

        self.fstring = "NUMBER OF AEROSOLS MODES: %i\n" % self._nb_modes

        mode = 0
        for i in range(len(self.ratio_list)):
            if self.ratio_list[i] != 0:
                self.fstring += self.library.get_properties(mode, wavelength_simu, wavelength_ref, ratio_list[i], self.library.species_short[i], rh)
                mode += 1

    def to_file(self, path, short=False):
        fname = ''
        for i in range(len(self.ratio_list)):
            if short:
                if self.ratio_list[i] != 0:
                    fname += ("%s%03d" % (self.species_short[i], int(self.ratio_list[i]*100)))
            else:
                fname += ("%s%03d" % (self.species_short[i], int(self.ratio_list[i] * 100)))

        fname += "RH" + str(int(self.rh*100)) + ".aer"
        f = open(path + '/' + fname, 'w')
        f.write(self.fstring)
        f.close()
        return path + '/' + fname

test = None

if test is not None:
    ld = Aerosol()
    a = ld.get_properties(1, 0.560, 0.550, 0.5, "BC", 30)
    print(a)

    md= Model([0.25,0.1,0.1,0.05,0.20,0.20,0.10], 30, 0.560, 0.550)
    print(md.fstring)

    md.to_file("/home/colinj/tmpdir/")


    md2= Model([1.0,0.0,0.0,0,0.0,0.0,0.0], 30, 0.560, 0.550)

    toto = md2.to_file("/home/colinj/tmpdir/")
    print(md2.fstring)