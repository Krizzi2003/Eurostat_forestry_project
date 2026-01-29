import pandas as pd

def basic_function(
        final_df: pd.DataFrame,
        src_df: pd.DataFrame, 
        treespec: list, 
        prod_wd: list, 
        unit: str, 
        mapa: dict) -> pd.DataFrame:
    
    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    # filtriraj samo TOTAL 
    df = df[df["treespec"].isin(treespec)] # uzimamo samo ukupne vrste drveca
    df = df[df["stk_flow"].isin(["PRD"])] #uzimamo samo proizvodnju unutar drzava
    df = df[df["prod_wd"].isin(prod_wd)] # uzimamo samo taj proizvod
    df = df[df["unit"].isin([unit])] # uzimamo samo jedinicu tisuca m3, s obzirom da postoje drvni proizvodi za koje nepostoji jedinica tisuce m3 stavljam ovaj dio isto kao varijablu

    # uzmi samo godine koje te zanimaju u ovom slučaju samo 2021 i 2022
    years = ["2021", "2022"]
    keep_cols = ["country", "treespec", "stk_flow", "prod_wd", "unit"] + years
    df = df[keep_cols]

    # wide -> long: 2021/2022 u jedan stupac 'year'
    long = df.melt(
        id_vars=["country", "treespec", "stk_flow", "prod_wd", "unit"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    long["feature"] = (
        long["prod_wd"].map(mapa) + "_" +
        long["stk_flow"].map(mapa)
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    # merge na final_df (outer = unija država/godina)
    merged = final_df.merge(wide, on=["country", "year"], how="outer")
    return merged

def basic_function_without_treespec(
        final_df: pd.DataFrame,
        src_df: pd.DataFrame,
        prod_wd: list,
        unit: str,
        mapa: dict
    ) -> pd.DataFrame:

    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    # filtriranja (isto kao prije, samo bez treespec)
    df = df[df["stk_flow"].isin(["PRD"])]       # proizvodnja unutar država
    df = df[df["prod_wd"].isin(prod_wd)]        # proizvodi
    df = df[df["unit"].isin([unit])]            # jedinica

    # uzmi samo godine koje te zanimaju
    years = ["2021", "2022"]
    keep_cols = ["country", "stk_flow", "prod_wd", "unit"] + years
    df = df[keep_cols]

    # wide -> long
    long = df.melt(
        id_vars=["country", "stk_flow", "prod_wd", "unit"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    long["feature"] = (
        long["prod_wd"].map(mapa) + "_" +
        long["stk_flow"].map(mapa)
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    # merge na final_df (outer = unija država/godina)
    merged = final_df.merge(wide, on=["country", "year"], how="outer")
    return merged

def add_config_bark_features(final_df: pd.DataFrame, src_df: pd.DataFrame) -> pd.DataFrame:

    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    # filtriraj samo CONIF / NCONF 
    df = df[df["treespec"].isin(["CONIF", "NCONIF"])]

    # uzmi samo godine koje te zanimaju u ovom slučaju samo 2021 i 2022
    years = ["2021", "2022"]
    keep_cols = ["country", "treespec", "bark"] + years
    df = df[keep_cols]

    # wide -> long: 2021/2022 u jedan stupac 'year'
    long = df.melt(
        id_vars=["country", "treespec", "bark"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )
    long["year"] = long["year"].astype(int)

    # napravi ime feature-a iz treespec + bark
    treespec_map = {"CONIF": "con", "NCONIF": "ncon"}
    bark_map = {"OVBK": "ob", "UNBK": "ub"}

    long["feature"] = (
        long["treespec"].map(treespec_map)
        + "_"
        + long["bark"].map(bark_map)
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)  # zbraja vrijednosti, ali vraća NaN ako su sve vrijednosti NaN
    )

    wide = wide.reset_index()

    # merge na final_df (outer = unija država/godina)
    merged = final_df.merge(wide, on=["country", "year"], how="outer")

    return merged


def add_roundwood_by_ownership_features(final_df: pd.DataFrame, src_df: pd.DataFrame) -> pd.DataFrame:

    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    df = df[df["treespec"].isin(["TOTAL"])] # filtriram samo TOTAL treespec

    # uzmi samo godine koje te zanimaju u ovom slučaju samo 2021 i 2022
    years = ["2021", "2022"]
    keep_cols = ["country", "owner", "treespec"] + years    
    df = df[keep_cols]

    # wide -> long: 2021/2022 u jedan stupac 'year'
    long = df.melt(
        id_vars=["country", "owner", "treespec"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )
    long["year"] = long["year"].astype(int)

    gcols = ["country", "year"]

    # nazivnik: suma svih ownera po drzavi/godini (NaN ako su sve NaN)
    den = long.groupby(gcols)["value"].sum(min_count=1).rename("den")

    # brojnik: suma samo PRV po drzavi/godini
    num = (
        long.loc[long["owner"].eq("PRV")]
            .groupby(gcols)["value"]
            .sum(min_count=1)
            .rename("num")
    )

    ratio = pd.concat([num, den], axis=1).reset_index()

    # omjer; ako je den NaN -> NaN, ako je den 0 -> NaN
    ratio["private_forests_share"] = ratio["num"] / ratio["den"]
    ratio.loc[ratio["den"].eq(0), "private_forests_share"] = pd.NA

    wide = ratio[["country", "year", "private_forests_share"]]

    # merge na final_df 
    merged = final_df.merge(wide, on=["country", "year"], how="outer")
    return merged

def add_industrial_roundwood_by_species_features(final_df: pd.DataFrame, src_df: pd.DataFrame) -> pd.DataFrame:

    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    df = df[df["treespec"].isin(["TOTAL"])] # filtriram samo TOTAL treespec
    df = df[df["stk_flow"].isin(["IMP", "EXP"])] # filtriram samo import i export
    df = df[df["unit"].isin(["THS_M3"])] # filtriram samo jedinicu tisuca m3

    # uzmi samo godine koje te zanimaju u ovom slučaju samo 2021 i 2022
    years = ["2021", "2022"]
    keep_cols = ["country", "treespec", "stk_flow"] + years    
    df = df[keep_cols]

    # wide -> long: 2021/2022 u jedan stupac 'year'
    long = df.melt(
        id_vars=["country", "treespec", "stk_flow"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    gcols = ["country", "year"]

    # nazivnik: suma importova + exportova po drzavi/godini (NaN ako su sve NaN)
    den = long.groupby(gcols)["value"].sum(min_count=1).rename("den")

    # brojnik: suma samo importova po drzavi/godini
    num = (
        long.loc[long["stk_flow"].eq("IMP")]
            .groupby(gcols)["value"]
            .sum(min_count=1)
            .rename("num")
    )

    ratio = pd.concat([num, den], axis=1).reset_index()

    # omjer; ako je den NaN -> NaN, ako je den 0 -> NaN
    ratio["industrial_import/export_share"] = ratio["num"] / ratio["den"]
    ratio.loc[ratio["den"].eq(0), "industrial_import/export_share"] = pd.NA

    wide = ratio[["country", "year", "industrial_import/export_share"]]

    # merge na final_df 
    merged = final_df.merge(wide, on=["country", "year"], how="outer")
    return merged

def add_sawnwood_trade_species_features(final_df: pd.DataFrame, src_df: pd.DataFrame) -> pd.DataFrame:

    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    df = df[df["treespec"].isin(["TOTAL"])] # filtriram samo TOTAL treespec
    df = df[df["stk_flow"].isin(["IMP", "EXP"])] # filtriram samo import i export
    df = df[df["unit"].isin(["THS_M3"])] # filtriram samo jedinicu tisuca m3

    # uzmi samo godine koje te zanimaju u ovom slučaju samo 2021 i 2022
    years = ["2021", "2022"]
    keep_cols = ["country", "treespec", "stk_flow"] + years    
    df = df[keep_cols]

    # wide -> long: 2021/2022 u jedan stupac 'year'
    long = df.melt(
        id_vars=["country", "treespec", "stk_flow"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    gcols = ["country", "year"]

    # nazivnik: suma importova + exportova po drzavi/godini (NaN ako su sve NaN)
    den = long.groupby(gcols)["value"].sum(min_count=1).rename("den")

    # brojnik: suma samo importova po drzavi/godini
    num = (
        long.loc[long["stk_flow"].eq("IMP")]
            .groupby(gcols)["value"]
            .sum(min_count=1)
            .rename("num")
    )

    ratio = pd.concat([num, den], axis=1).reset_index()

    # omjer; ako je den NaN -> NaN, ako je den 0 -> NaN
    ratio["sawnwood_import/export_share"] = ratio["num"] / ratio["den"]
    ratio.loc[ratio["den"].eq(0), "sawnwood_import/export_share"] = pd.NA

    wide = ratio[["country", "year", "sawnwood_import/export_share"]]

    # merge na final_df 
    merged = final_df.merge(wide, on=["country", "year"], how="outer")
    return merged


def economic_aggregates_of_forestry(
        final_df: pd.DataFrame,
        src_df: pd.DataFrame,
        mapa: dict
    ) -> pd.DataFrame:

    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    #uzimam samo B1G I P1, te milione eura kao jedinicu
    df = df[df["for_acc"].isin(["B1G", "P1"])]      
    df = df[df["unit"].isin(["MIO_EUR"])]

    # uzmi samo godine koje te zanimaju
    years = ["2021", "2022"]
    keep_cols = ["country", "for_acc"] + years
    df = df[keep_cols]

    # wide -> long
    long = df.melt(
        id_vars=["country", "for_acc"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    long["feature"] = (
        long["for_acc"].map(mapa)
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    # merge na final_df (outer = unija država/godina)
    merged = final_df.merge(wide, on=["country", "year"], how="left")
    return merged

def add_awu_forestry_logging_features(final_df: pd.DataFrame, src_df: pd.DataFrame) -> pd.DataFrame:
    df = src_df.copy()
    base = final_df.copy()

    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    years = ["2021", "2022"]
    keep_cols = ["country", "unit"] + years
    df = df[keep_cols]

    # wide -> long
    long = df.melt(
        id_vars=["country", "unit"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )
    long["year"] = long["year"].astype(int)

    # suma po drzavi/godini (NaN ako su sve NaN)
    summed = (long.groupby(["country", "year"], as_index=False)["value"]
              .sum(min_count=1)
              .rename(columns={"value": "awu_total"}))

    final_cols = base[["country", "year",
                       "output_of_forestry_mil_euro",
                       "value_added_forestry_mil_euro"]]

    ratio = summed.merge(final_cols, on=["country", "year"], how="left")

    ratio["output_per_awu"] = ratio["output_of_forestry_mil_euro"] / ratio["awu_total"]
    ratio["gva_per_awu"] = ratio["value_added_forestry_mil_euro"] / ratio["awu_total"]

    features = ratio[["country", "year", "awu_total", "output_per_awu", "gva_per_awu"]]

    # merge na final_df
    merged = final_df.merge(features, on=["country", "year"], how="left")
    return merged

def roundwood_fuelwood_basic_imp_exp_features(final_df: pd.DataFrame, src_df: pd.DataFrame, mapa: dict) -> pd.DataFrame:
    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    #Filtriram samo total, kubične metre i import/export 
    df = df[df["treespec"].isin(["TOTAL"])]
    df = df[df["stk_flow"].isin(["IMP", "EXP"])]
    df = df[df["unit"].isin(["THS_M3"])]

    # uzmi samo godine koje te zanimaju
    years = ["2021", "2022"]
    keep_cols = ["country", "treespec", "stk_flow", "unit"] + years
    df = df[keep_cols]

    # wide -> long
    long = df.melt(
        id_vars=["country", "treespec", "stk_flow", "unit"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    long["feature"] = (
        "basic_wood_products_" + 
        long["stk_flow"].map(mapa)
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    # merge na final_df (outer = unija država/godina)
    merged = final_df.merge(wide, on=["country", "year"], how="outer")
    return merged

def secondary_wood_trade_add_features(final_df: pd.DataFrame, src_df: pd.DataFrame, mapa: dict) -> pd.DataFrame:
    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    #Filtriram samo total, kubične metre i import/export 
    df = df[df["treespec"].isin(["TOTAL"])]
    df = df[df["unit"].isin(["THS_EUR"])]
    df = df[df["prod_wd"].isin(["SW"])]

    # uzmi samo godine koje te zanimaju
    years = ["2021", "2022"]
    keep_cols = ["country", "treespec", "prod_wd", "unit", "stk_flow"] + years
    df = df[keep_cols]

    # wide -> long
    long = df.melt(
        id_vars=["country", "treespec", "prod_wd", "unit", "stk_flow"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    long["feature"] = (
        "secondary_wood_trade_" +
        long["stk_flow"].map(mapa) 
        
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    # merge na final_df (outer = unija država/godina)
    merged = final_df.merge(wide, on=["country", "year"], how="outer")
    return merged

def secondary_paper_products_features(final_df: pd.DataFrame, src_df: pd.DataFrame, mapa: dict) -> pd.DataFrame:
    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})


    #imp/exp u tisucama eura eurima 
    df = df[df["stk_flow"].isin(["IMP", "EXP", "EXP_XEU", "IMP_XEU"])] # filtriram samo import i export
    df = df[df["unit"].isin(["THS_EUR"])] # filtriram samo jedinicu tisuca eura
    df = df[df["prod_wd"].isin(["SP"])] #uzimam samo secondary paper products

    # uzmi samo godine koje te zanimaju u ovom slučaju samo 2021 i 2022
    years = ["2021", "2022"]
    keep_cols = ["country", "stk_flow", "prod_wd", "unit"] + years    
    df = df[keep_cols]

    # wide -> long: 2021/2022 u jedan stupac 'year'
    long = df.melt(
        id_vars=["country", "stk_flow", "prod_wd", "unit"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    long["feature"] = (
        "secondary_paper_products_" +
        long["stk_flow"].map(mapa) 
        
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()


    # merge na final_df (outer = unija država/godina)
    merged = final_df.merge(wide, on=["country", "year"], how="outer")
    return merged

def secondary_wood_products_features(final_df: pd.DataFrame, src_df: pd.DataFrame) -> pd.DataFrame:
    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    # filtriraj samo total, kubične metre 
    df = df[df["unit"].isin(["THS_M3"])]
    df = df[df["prod_wd"].isin(["GLT_CLT"])]

    # uzmi samo godine koje te zanimaju
    years = ["2021", "2022"]
    keep_cols = ["country", "prod_wd", "unit"] + years
    df = df[keep_cols]

    # wide -> long
    long = df.melt(
        id_vars=["country", "prod_wd", "unit"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    long["feature"] = (
        "secondary_wood_products_production" 
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    merged = final_df.merge(wide, on=["country", "year"], how="outer")
    return merged


def employment_features(final_df: pd.DataFrame, src_df: pd.DataFrame) -> pd.DataFrame:
    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    # filtriraj samo total, broj zaposlenih 
    df = df[df["sex"].isin(["T"])]
    df = df[df["isced11"].isin(["TOTAL", "ED5-8"])]
    df = df[df["wstatus"].isin(["EMP"])]


    # uzmi samo godine koje te zanimaju
    years = ["2021", "2022"]
    keep_cols = ["country", "isced11", "wstatus", "nace_r2"] + years
    df = df[keep_cols]

    # wide -> long
    long = df.melt(
        id_vars=["country", "isced11", "wstatus", "nace_r2"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)


    long["feature"] = (
        "employment" + long["isced11"].map({"TOTAL": "_all_education_levels", "ED5-8": "_high_education_levels"})
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    #omjer visokoeduciranih i svih zaposlenih
    wide["high_education_emp/all_emp_share"] = wide["employment_high_education_levels"] / wide["employment_all_education_levels"]
    wide.drop(columns=["employment_high_education_levels", "employment_all_education_levels"], inplace=True)

    #ubacujem stupac omjera visokoeduciranih i svih zaposlenih u tablicu i idem dalje
    merged = final_df.merge(wide, on=["country", "year"], how="left")

    #--------------------------
    #krecem izradu stupaca za razlicite aktivnosti u sumarstvu (nace_r2)

    long["feature"] = (
        long["nace_r2"].map(
            {
            "A02" : "employment_forestry_logging",
            "C16" : "employment_manufacturing_wood_products",
            "C17" : "employment_manufacturing_paper_products",
            "C31" : "employment_manufacturing_furniture"}
        )
    )

    long = long[long["isced11"] == "TOTAL"]

    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    merged = merged.merge(wide, on=["country", "year"], how="left")

    return merged


def generation_of_waste_features(final_df: pd.DataFrame, src_df: pd.DataFrame) -> pd.DataFrame:
    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    df = df[df["unit"].isin(["T"])] # filtriram samo po tonama
    df = df[df["hazard"].isin(["HAZ_NHAZ"])] # uzimam i hazardni i nehazardni otpad
    df = df[df["nace_r2"].isin(["A"])] # uzimam samo podatke vezane za sektor A - Agriculture, forestry and fishing

    years = ["2022"]
    keep_cols = ["country", "waste", "unit", "hazard", "nace_r2"] + years
    df = df[keep_cols]

    # wide -> long
    long = df.melt(
        id_vars=["country", "waste", "unit", "hazard", "nace_r2"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    long["feature"] = (
        "generation_of_waste_" + long["waste"].map(
            {
                "W075": "wood",
                "W072": "paper"
            }
        )
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    merged = final_df.merge(wide, on=["country", "year"], how="left")
    return merged

def treatment_of_waste_features(final_df: pd.DataFrame, src_df: pd.DataFrame) -> pd.DataFrame:
    df = src_df.copy()

    # preimenuj geo kolonu u 'country'
    if "geo\\TIME_PERIOD" in df.columns:
        df = df.rename(columns={"geo\\TIME_PERIOD": "country"})

    df = df[df["unit"].isin(["T"])] # filtriram samo po tonama
    df = df[df["hazard"].isin(["HAZ_NHAZ"])] # uzimam i hazardni i nehazardni otpad
    df = df[df["wst_oper"].isin(["TRT"])] # uzimam samo podatke vezane za waste treatment

    years = ["2022"]
    keep_cols = ["country", "waste", "unit", "hazard", "wst_oper"] + years
    df = df[keep_cols]

    # wide -> long
    long = df.melt(
        id_vars=["country", "waste", "unit", "hazard", "wst_oper"],
        value_vars=years,
        var_name="year",
        value_name="value"
    )

    long["year"] = long["year"].astype(int)

    long["feature"] = (
        "treatment_of_waste_" + long["waste"].map(
            {
                "W075": "wood",
                "W072": "paper"
            }
        )
    )

    # pivot: jedan red = (country, year), stupci = feature-i
    wide = long.pivot_table(
        index=["country", "year"],
        columns="feature",
        values="value",
        aggfunc=lambda s: s.sum(min_count=1)
    ).reset_index()

    merged = final_df.merge(wide, on=["country", "year"], how="left")
    return merged