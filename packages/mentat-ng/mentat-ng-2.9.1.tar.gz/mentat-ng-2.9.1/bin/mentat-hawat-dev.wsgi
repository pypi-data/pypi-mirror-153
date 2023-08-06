#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


from dotenv import load_dotenv

import hawat

load_dotenv(dotenv_path = '/home/mentat/mentat-ng/.env')

#
# Use prepared factory function to create application instance. The factory
# function takes number of arguments, that can be used to fine tune configuration
# of the application. This is can be very usefull when extending applications`
# capabilities or for purposes of testing. Please refer to the documentation
# for more information.
#

application = hawat.create_app()
