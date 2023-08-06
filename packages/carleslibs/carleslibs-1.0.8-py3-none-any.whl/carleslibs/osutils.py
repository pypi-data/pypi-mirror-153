import os


class OsUtils:

    s_platform_hostname = ""
    s_platform_system = ""
    s_platform_release = ""
    s_platform_machine = ""
    s_platform_version = ""

    s_distrib_description = ""

    o_fileutils = None

    b_is_in_amazon = False
    b_is_in_docker = False
    b_is_in_lxc = False
    b_is_in_virtualbox = False
    b_is_in_openstack = False
    b_is_in_google = False

    b_error_accessing_dmi = False

    def __init__(self, o_fileutils=None):
        self.detect_system()

        self.o_fileutils = o_fileutils
        self.update_distribution_details()

        if self.is_linux() is True:
            # This will make fail on Mac
            self.update_is_in_docker()
            self.update_is_in_lxc()
            self.update_is_in_vbox_or_amazon_or_gcp()
            self.update_is_in_openstack()

    def detect_system(self):
        """
        Detects the basic architecture of the system and update instance variables.
        :return:
        """

        # In Python 3 is like:
        # posix.uname_result(sysname='Linux', nodename='fast', release='5.4.0-65-generic',
        #                    version='#73-Ubuntu SMP Mon Jan 18 17:25:17 UTC 2021',
        #                    machine='x86_64')
        # In Python 2 just a list.

        # self.s_platform_system = os.uname().sysname
        self.s_platform_system = os.uname()[0]

        # self.s_platform_hostname = os.uname().nodename
        self.s_platform_hostname = os.uname()[1]

        # 5.3.0-23-generic
        # self.s_platform_release = os.uname().release
        self.s_platform_release = os.uname()[2]

        # x86_64
        # self.s_plaform_machine = os.uname().machine
        self.s_plaform_machine = os.uname()[3]

        # self.s_plaform_version = os.uname().version
        self.s_plaform_version = os.uname()[4]

    def update_distribution_details(self):

        self.s_distrib_description = ""

        b_success, s_contents = self.o_fileutils.read_file_as_string("/etc/lsb-release")

        if b_success is True:
            a_s_contents = s_contents.split("\n")

            for s_line in a_s_contents:
                a_s_line = s_line.split("=")
                if len(a_s_line) > 1:
                    if a_s_line[0] == "DISTRIB_DESCRIPTION":
                        self.s_distrib_description = a_s_line[1].replace('"', '')

    def update_is_in_docker(self):
        """
        Returns: True if running in a Docker container, else False
        :return:
        """
        self.b_is_in_docker = False

        b_success, s_contents = self.o_fileutils.read_file_as_string("/proc/1/cgroup")

        self.b_is_in_docker = 'docker' in s_contents

    def update_is_in_lxc(self):
        """
        Returns: True if running in a LXC container, else False
        :return:
        """
        self.b_is_in_lxc = False

        b_success, s_contents = self.o_fileutils.read_file_as_string("/proc/1/cgroup")

        self.b_is_in_lxc = 'lxc' in s_contents

    def update_is_in_openstack(self):

        self.b_is_in_openstack = False

        b_success, s_strings = self.o_fileutils.strings('/sys/firmware/dmi/tables/DMI')

        if b_success is True:
            s_strings = s_strings.lower()
            self.b_is_in_openstack = 'openstack' in s_strings
        else:
            self.b_error_accessing_dmi = True

    def update_is_in_vbox_or_amazon_or_gcp(self):
        """"
        Update the booleans if VirtualBox, Amazon or Google VMs are detected
        """

        self.b_is_in_virtualbox = False

        b_success, s_strings = self.o_fileutils.strings('/sys/firmware/dmi/tables/DMI')

        if b_success is True:
            s_strings = s_strings.lower()
            self.b_is_in_virtualbox = 'virtualbox' in s_strings
            self.b_is_in_amazon = 'amazon' in s_strings
            self.b_is_in_google = 'google' in s_strings
        else:
            self.b_error_accessing_dmi = True

    def get_distribution_description(self):
        return self.s_distrib_description

    def get_platform_system(self):
        return self.s_platform_system

    def get_platform_release(self):
        return self.s_platform_release

    def is_linux(self):
        if self.get_platform_system().lower() == "linux":
            return True
        else:
            return False

    def get_platform_hostname(self):
        return self.s_platform_hostname

    def get_platform_machine(self):
        return self.s_plaform_machine

    def get_platform_version(self):
        return self.s_plaform_version

    def get_is_in_amazon(self):
        return self.b_is_in_amazon

    def get_is_in_google(self):
        return self.b_is_in_google

    def get_is_in_openstack(self):
        return self.b_is_in_openstack

    def get_is_in_virtualbox(self):
        return self.b_is_in_virtualbox

    def get_is_in_docker(self):
        return self.b_is_in_docker

    def get_is_in_lxc(self):
        return self.b_is_in_lxc

    def get_error_accessing_dmi(self):
        return self.b_error_accessing_dmi

    def get_uptime(self):
        b_success, s_uptime = self.o_fileutils.read_file_as_string('/proc/uptime')
        if b_success is True:
            s_uptime_seconds = str(int(float(s_uptime.split()[0])))
        else:
            s_uptime_seconds = ""

        return b_success, s_uptime_seconds

    def get_total_and_free_space_in_bytes(self, s_folder='/'):
        d_sf_data = os.statvfs(s_folder)
        f_total_bytes = d_sf_data.f_blocks * d_sf_data.f_frsize
        f_free_bytes = d_sf_data.f_bavail * d_sf_data.f_frsize

        return f_total_bytes, f_free_bytes

    def get_total_and_free_space_in_gib(self, s_folder='/', b_add_units=True):
        """
        Returns the Free Space in GiB with two decimals.
        Compatible with Python 3 and Python 2.
        @param s_folder:
        @param b_add_units:
        @return: float, float, string, string
        """
        i_total_bytes, i_free_bytes = self.get_total_and_free_space_in_bytes(s_folder)
        f_total_gb = round(i_total_bytes / 1024.0 / 1024.0 / 1024.0, 2)
        f_free_gb = round(i_free_bytes / 1024.0 / 1024.0 / 1024.0, 2)
        s_total_gb = str(f_total_gb)
        s_free_gb = str(f_free_gb)
        i_total_gb  = int(f_total_gb)
        i_free_gb = int(f_free_gb)
        if b_add_units is True:
            s_free_gb = s_free_gb + "GiB"
            s_total_gb = s_total_gb + "GiB"

        return f_total_gb, f_free_gb, s_total_gb, s_free_gb

    def get_inodes_in_use_and_free(self, s_folder='/'):
        """
        Returns the total inodes, the free ones, and percentage of inodes free
        """
        d_sf_data = os.statvfs(s_folder)

        i_total_inode = d_sf_data.f_files        # inodes
        i_free_inode = d_sf_data.f_ffree   #free inodes

        f_percent_free = (100.0 * i_free_inode)/i_total_inode

        return i_total_inode, i_free_inode, f_percent_free

    def get_partition_type_for_mountpoint(self, s_path='/'):
        s_file = '/etc/fstab'

        b_success, s_contents = self.o_fileutils.read_file_as_string(s_file)

        if b_success is False:
            return False, ""

        # Replace tabs by spaces to make it easier to find the path
        s_contents = s_contents.replace("\t", ' ')
        a_s_lines = s_contents.split("\n")

        s_path_to_find = " " + s_path + " "
        b_success = False
        s_type = ""
        for s_line in a_s_lines:
            if s_line == "":
                continue

            if s_line[0] == '#':
                # Is a comment. We don't want something interferring like:
                # # / was on /dev/nvme0n1p2 during installation
                continue
            i_pos_found = s_line.find(s_path_to_find)
            s_type = ""
            if i_pos_found > -1:
                b_success = True
                # Get from after / to the end of the line
                s_rest_of_fstab_line = s_line[i_pos_found + len(s_path_to_find):]
                a_fields = s_rest_of_fstab_line.split()
                s_type = a_fields[0]
                break

        return b_success, s_type

    def get_euid(self):
        i_userid = os.geteuid()

        return i_userid

    def get_username(self):
        b_success = False
        s_username = ""

        if "USER" in os.environ:
            b_success = True
            s_username = os.environ["USER"]

        return b_success, s_username
