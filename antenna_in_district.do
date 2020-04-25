cls
/*
Do file for attaching Ubigeos (Peruvian Location Code) to antenna's locations
Programmer: Marco Gutierrez
*/

set more off
clear all

global root="D:\Work Archives\Trabajo\GECE - LEEX\Kristian\Covid19\covid-scraping-peru"
cap mkdir "$root\distritos"
global distritos="$root\distritos"
cd "$root"
************************************
*! -point2poly-: Assigns points to polygons                                    
*! Version 1.0.0 - 25 April 2010                                               
*! Author: Maurizio Pisati                                                     
*! Department of Sociology and Social Research                                 
*! University of Milano Bicocca (Italy)                                        
*! maurizio.pisati@unimib.it                                                   




*  ----------------------------------------------------------------------------
*  Main program                                                                
*  ----------------------------------------------------------------------------

program point2poly
version 11

syntax using/,                     ///
       ID(varname numeric)         ///
       Xcoord(varname numeric)     ///
       Ycoord(varname numeric)     ///
       Polyname(name)

preserve
qui use "`using'", clear
qui drop if _X==.
tempfile POLY1
qui save `POLY1', replace
tempvar IDX
qui gen `IDX' = _n
collapse (min) xmin=_X ymin=_Y fn=`IDX' (max) xmax=_X ymax=_Y ln=`IDX', by(_ID)
qui rename _ID poly
tempfile POLY2
qui save `POLY2', replace
restore

preserve
keep `id' `xcoord' `ycoord'
qui gen _POLY = .
qui merge using `POLY1'
qui drop _merge
qui merge using `POLY2'
qui drop _merge
order `id' `xcoord' `ycoord' _POLY _ID _X _Y poly xmin xmax ymin ymax fn ln
qui summarize `id'
local NPOINTS = r(N)
qui summarize poly
local NPOLY = r(N)
di ""
mata: point2poly(`NPOINTS', `NPOLY', "dots")
keep `id' _POLY
rename _POLY `polyname'
qui drop if `id'==.
tempfile POLY3
qui save `POLY3', replace
restore

qui merge 1:1 `id' using `POLY3'
qui drop _merge

end




*  ----------------------------------------------------------------------------
*  Mata functions                                                              
*  ----------------------------------------------------------------------------

version 10.1
mata:
mata clear
mata set matastrict on


void point2poly(real scalar nc, real scalar np, string scalar dots)
{

real scalar   c, x, y, p, xmin, xmax, ymin, ymax, fn, ln
real matrix   POLY
if (dots != "") sp_dots1("Points", nc)
for (c=1; c<=nc; c++) {
   if (dots != "") sp_dots2(c, nc)
   x = _st_data(c, 2)
   y = _st_data(c, 3)
   for (p=1; p<=np; p++) {
      xmin = _st_data(p, 9)
      xmax = _st_data(p, 10)
      ymin = _st_data(p, 11)
      ymax = _st_data(p, 12)
      if (x>=xmin & x<=xmax & y>=ymin & y<=ymax) {
         fn = _st_data(p, 13)
         ln = _st_data(p, 14)
         POLY = st_data((fn,ln), (6,7))
         if (sp_pips(x, y, POLY)) {
            st_store(c, 4, _st_data(p, 8))
            break
         }
      }
   }
}

}


void sp_dots1(string scalar header, real scalar n)
{

printf("{txt}%s (", header)
printf("{res}%g{txt})\n", n)
printf("{txt}{hline 4}{c +}{hline 3} 1 {hline 3}{c +}{hline 3} 2 ")
printf("{txt}{hline 3}{c +}{hline 3} 3 {hline 3}{c +}{hline 3} 4 ")
printf("{txt}{hline 3}{c +}{hline 3} 5\n")

}


void sp_dots2(real scalar i, real scalar n)
{

real scalar   linenum
linenum = mod(i,50)
if (linenum != 0  &  i < n) {
   printf("{txt}.")
}
if (linenum == 0  &  i < n) {
   printf("{txt}. %5.0f\n", i)
}
if (i == n) {
   printf("{txt}.\n")
   printf("\n")
}

}


real scalar sp_pips(real scalar x, real scalar y, real matrix POLY)
{

real scalar   pip, nv, iwind, xlastp, ylastp, ioldq, inewq
real scalar   xthisp, ythisp, i, a, b
nv = rows(POLY)
if (POLY[1,1] == POLY[nv,1] & POLY[1,2] == POLY[nv,2]) nv = nv - 1
iwind = 0
xlastp = POLY[nv, 1]
ylastp = POLY[nv, 2]
ioldq = sp_pips_aux(xlastp, ylastp, x, y)
for (i=1; i<=nv; i++) {
   xthisp = POLY[i, 1]
   ythisp = POLY[i, 2]
   inewq = sp_pips_aux(xthisp, ythisp, x, y)
   if (ioldq != inewq) {
      if (mod(ioldq+1, 4) == inewq) {
         iwind = iwind + 1
      }
      else if (mod(inewq+1, 4) == ioldq) {
         iwind = iwind - 1
      }
      else {
         a = (ylastp - ythisp) * (x - xlastp)
         b = xlastp - xthisp
         a = a + ylastp * b
         b = b * y
         if (a > b) {
            iwind = iwind + 2
         }
         else {
            iwind = iwind - 2
         }
      }
   }
   xlastp = xthisp
   ylastp = ythisp
   ioldq = inewq
}
pip = abs(iwind / 4)
return(pip)

}


real scalar sp_pips_aux(real scalar xp, real scalar yp, real scalar xo,
                        real scalar yo)
{

real scalar iq
if(xp < xo) {
   if(yp < yo) iq = 2
   else iq = 1
}
else {
   if(yp < yo) iq = 3
   else iq = 0
}
return(iq)

}


end
************************************

shp2dta using "$distritos\DISTRITOS.shp", data("$distritos\distritos_peru_shp") coord("$distritos\distritos_peru_coords") replace

import delimited "antennas_adresses.csv"
generate id = _n

*Y es latitud y X longitud
spmap using "$distritos\distritos_peru_coords.dta", id(id) point(x(longitude) y(latitude) fcolor(red) size(*0.6))
point2poly using "$distritos\distritos_peru_coords.dta", id(id) x(longitude) y(latitude) polyname(district)
spmap using "$distritos\distritos_peru_coords.dta", id(id) label(x(longitude) y(latitude) color(red) label(district) size(*0.8))

rename district distr_code

*save antennas_districts, replace

use antennas_districts, clear

preserve
	use "$distritos\distritos_peru_shp.dta", clear
	keep _ID PROVINCIA DISTRITO DEPARTAMEN IDDIST
	rename _ID distr_code
	rename IDDIST ubigeo
	save "distritos\id_shp_districts.dta", replace
restore

drop ubigeo
merge m:1 distr_code using "distritos\id_shp_districts.dta", keep(3) nogen

drop address
egen address = concat(DISTRITO PROVINCIA DEPARTAMEN), punct(", ")
drop DISTRITO PROVINCIA DEPARTAMEN

export excel using "$root\antennas_ubigeos.xls", firstrow(variables) replace
