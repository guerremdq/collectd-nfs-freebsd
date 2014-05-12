collectd-nfs-freebsd
====================

NFS Plugin for collectd and FreeBSD

configuration 


            <Plugin python>
                ModulePath "/opt/collectd/plugins/python/"
                LogTraces true
                Interactive false
                Import "nfs_stats"

                <Module nfs_stats>
                </Module>
            </Plugin>

