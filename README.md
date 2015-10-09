# check_mk_tools
Tools for working with Check_MK


For Check_MK Agent with Systemd
add check_mk@.service and check_mk.socket to /lib/systemd/system/
service check_mk.socket [re]start
systemctl restart sockets.target
