cls
clear all
set more off

cd "D:\Work Archives\Trabajo\GECE - LEEX\Kristian\Covid19\covid-scraping-peru"

**Distances
import excel "prov_distances_ubigeos.xlsx", sheet("Sheet1") firstrow allstring
foreach variab of varlist _all{
	cap replace `variab' = subinstr(`variab', " km", "",.)
}
export excel using "prov_distances_ubigeos_num.xlsx", firstrow(varlabels) replace

**Times
clear 
import excel "prov_times_ubigeos.xlsx", sheet("Sheet1") firstrow allstring

unab allvars: _all
loc vars_to_exclude "OriginProvinceDestinationProv"
foreach variab in `:list allvars - vars_to_exclude'{
	*Días
	gen `variab'_day = ""
	gen `variab'_day_pos = strpos(`variab', "d")
	replace `variab'_day = "0" if `variab'_day_pos==0
	replace `variab'_day = strtrim(substr(`variab', 1, `variab'_day_pos - 1)) if `variab'_day_pos!=0
	destring(`variab'_day), replace
	replace `variab'_day = `variab'_day*24

	*Horas
	gen `variab'_hour = ""
	gen `variab'_hour_pos = strpos(`variab', "h")
	replace `variab'_hour = "0" if `variab'_hour_pos==0
	replace `variab'_hour = strtrim(substr(`variab', `variab'_hour_pos-3, 3)) if `variab'_hour_pos>3
	replace `variab'_hour = strtrim(substr(`variab', `variab'_hour_pos-2, 2)) if `variab'_hour_pos==3
	destring(`variab'_hour), replace

	*Minutos
	gen `variab'_min = ""
	gen `variab'_min_pos = strpos(`variab', "m")
	replace `variab'_min = "0" if `variab'_min_pos==0
	replace `variab'_min = strtrim(substr(`variab', `variab'_min_pos-3, 3)) if `variab'_min_pos!=0
	replace `variab'_min = strtrim(substr(`variab', `variab'_min_pos-2, 2)) if `variab'_min_pos==3
	destring(`variab'_min), replace
	replace `variab'_min = `variab'_min/60

	*Total en Horas
	gen `variab'_total = `variab'_day+`variab'_hour+`variab'_min
	tostring(`variab'_total), replace force
	forval i = 3(-1)1{
		local j = `i'+1
		replace `variab'_total = substr(`variab'_total,1,`j') if strpos(`variab'_total, ".") == `i'	
	}
	replace `variab'_total = `variab'_total + ".0" if strpos(`variab'_total, ".") == 0

	replace `variab' = `variab'_total
	drop *_*
}

export excel using "prov_times_ubigeos_num.xlsx", firstrow(varlabels) replace
