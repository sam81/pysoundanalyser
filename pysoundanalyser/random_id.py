# -*- coding: utf-8 -*-
#   Copyright (C) 2010-2024 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pysoundanalyser

#    pysoundanalyser is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pysoundanalyser is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pysoundanalyser.  If not, see <http://www.gnu.org/licenses/>.

import string, random
#generate random string of length n
def random_id(n=3, id_type="alphanumeric"):
    if id_type == "numeric":
        rand_id = [random.choice(string.digits) for x in range(n)]
    elif id_type == "alphabetic":
        rand_id = [random.choice(string.ascii_letters) for x in range(n)]
    elif id_type == "alphanumeric":
        rand_id = [random.choice(string.ascii_letters + string.digits) for x in range(n)]
    rand_id = "".join(rand_id)
    return rand_id

    
