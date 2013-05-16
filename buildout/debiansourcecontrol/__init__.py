import os
import errno
import logging
import shutil

LOG = logging.getLogger("buildout.debiansourcecontrol")


class Check(object):
    def __init__(self, buildout):
        self.buildout = buildout
        self.parts_buildout = buildout['buildout']
        self.bdirectory = buildout['buildout']['directory']

    def check_directory_inside(self, d):
        if not d:
            msg = "You must set an %s inside the buildout" % d
            raise ValueError(msg)
        elif d.startswith('/') and not d.startswith(self.bdirectory):
                msg = "Please use related path for %s" % d
                raise ValueError(msg)

    def extends_cache(self):
        self.check_directory_inside(self.parts_buildout.get('extends-cache'))

    def eggs_directory(self):
        self.check_directory_inside(self.parts_buildout.get('eggs-directory'))

    def download_cache(self):
        self.check_directory_inside(self.parts_buildout.get('download-cache'))

def start(buildout):
    """
    if any of the following constraints are false, it raises an exception

    * check extends-cache is insinde the buildout
    * check eggs-directory is inside the buildout
    * check download-cache is inside the buildout

    """
    check = Check(buildout)
    check.extends_cache()
    check.eggs_directory()
    check.download_cache()


class DebianSourceControl(object):
    def __init__(self, buildout):
        self.buildout = buildout
        self.cwd = buildout['buildout']['directory']

    def ignore(self, directory, files):
        """
        will receive as its arguments the directory being visited by
        copytree(), and a list of its contents, as returned by os.listdir().
        
        will be called once for each directory that is copied. 
        
        return a sequence of directory and file names relative to the current
        directory (i.e. a subset of the items in its second argument); 
        these names will then be ignored in the copy process. 
        shutil.ignore_patterns() can be used to create such a callable that
        ignores names based on glob-style patterns.
        """
        ignore_list = []
        ignores = ('build', 'var')
        build = os.path.join(directory, 'build')
        var = os.path.join(directory, 'var')
        for filename in files:
            full_path = os.path.join(directory, filename)
            if full_path.startswith(build):
                ignore_list.append(filename)
            if full_path.startswith(var):
                ignore_list.append(filename)

        return ignore_list

    def copytree(self, src, dst, symlinks=False, ignore=None):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst, symlinks=symlinks, ignore=ignore)

    def init_structure(self):
        """This create the debian source control minimal tree structure
        based on the current buildout folder.
        It also copy the buildout DEBIAN folder to the package"""
        dest = os.path.join(self.cwd, 'build', 'debian')
        self.mkdir_p(dest)
        struct = os.path.join(dest, self.cwd)
        self.mkdir_p(struct)
#        copytree_src = os.path.join(self.cwd, 'DEBIAN')
#        self.copytree(copytree_src, dest, symlinks=False, ignore=None)

        new_dest = os.path.join(dest, self.cwd[1:])
        self.copytree(
            self.cwd,
            new_dest,
            symlinks=False,
            ignore=self.ignore
        )

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as error:
            if error.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

    def update_md5sum(self):
        pass

    def update_chmod(self):
        """if scripts are not executable, make them executable"""
        pass


def finish(buildout):
    """
    This do the job to create the structure
    """
    dsc = DebianSourceControl(buildout)
    dsc.init_structure()
