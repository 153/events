#!/bin/python3

import cgi, cgitb
import os, os.path
import calendar, time, datetime
import mistune, math

markdown = mistune.markdown
calendar.setfirstweekday(calendar.SUNDAY)
cgitb.enable()

year = datetime.datetime.now().year

months = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04",
"May":"05", "Jun":"06", "Jul":"07", "Aug":"08",
"Sep":"09", "Oct":"10", "Nov": "11", "Dec":"12"}

def escape_html(text):
        """escape strings for display in HTML"""
        if text:
            return cgi.escape(text, quote=True).\
            replace(u'\t', u'&emsp;').\
            replace(u'  ', u' &nbsp;').\
            replace(u'<', u'&lt;').\
            replace(u'>', u'&gt;').\
            replace(u'|', u'l').\
            replace(u'\n', u'<br>').\
            replace(u'\r', u'').\
            replace(u'&lt;br&gt;', u'<br>')

def events_view(group_key="blank"):
    print("<h2>events: Event Listing</h2>")
    with open("list.html") as t:
        print(t.read())
    events_list = []
    for root, dirnames, filenames in os.walk("./data/"):
        for filename in filenames:
            if filename[-4:] == ".txt":
                with open(os.path.join(root, filename)) as e_i:
                    lines = e_i.read().splitlines()
                    event_date = root[-2:] + lines[2][4:11]
                    event_name = os.path.join(root, filename)
                events_list.append((event_date+event_name))
    events_list = sorted(events_list)
    num = 0
    for event_item in events_list:
        num += 1
        with open(event_item[11:], 'r') as e_i:
            lines = e_i.read().splitlines()
            print("<tr><td>"+str(num)+".")
            lines[6] = lines[6].split(", ")
            memb_count = len(lines[6])
            peeps = []
            if memb_count == 1:
                peeps = lines[6][0]
            elif memb_count == 2:
                peeps = lines[6][0]+", "+lines[6][1]
            else:
                for i in lines[6][:2]:
                    peeps.append(i+", ")
                peeps.append(lines[6][2])
                if memb_count > 3:
                    peeps.append("...")
            peeps = str(memb_count)+": "+"".join(peeps)
            event_link = event_item.split("/")[-1][:-4]
            if lines[1][0] == "1":
                lines[2] = "<center>???</center>"
                peeps = "<center>" + ("----" * 3) + "</center>"
                lines[5] = "<img src='lock.png'" + \
                " style='height:18px; width:18px'>Private"
            print("<td><a href='?m=view;v={0}'>{1}</a><td>{2}".format(event_link, lines[0], lines[2]))
            print("<td><center>{0}</center><td>{1}".format(lines[5], peeps))
            print("</tr>")
    print("</table></div>")

def event_edit(event_name, guest_name, pub_string='', group_key='',confirm_create='0', pb_status=None):
    row_modded = 0
    for root, dirnames, filenames in os.walk("./data/"):
        for filename in filenames:
            if event_name == filename[:-4]:
                event_fil = str(os.path.join(root, filename))
                with open(os.path.join(root, filename)) as ur_event:
                    lines = ur_event.read().splitlines()
                    print("<h1>Events: " + lines[0]+"</h1>")
                    guest_list = list(lines[6].split(", "))
                    if guest_name in guest_list:
                        print("You're already attending this event, silly goose.")
                        print('<p><a href="?m=view;v=' + filename[:-4] + '">')
                        print('&larr; back</a>')
                        print('<br><a href="?m=view">&larr; &larr; events</a>')
                        print('<br><a href="?">&larr; &larr; &larr; home</a>')
                        pass
                    else:
                        guest_list.append(guest_name)
                        row_modded = 1

        if pub_string and group_key:
            pub_list = pub_string.split('|')
            pub_list[1] = pub_list[2]
            pub_list[2] = pub_list[3]
            pub_list[3] = markdown(pub_list[4])
            pub_list[4] = pub_list[6]
            pub_list.append(pub_list[6])
            pub_list.append("1")
            dir_mon = months[pub_list[1].split(" ")[0]]
            fil_nam = ''.join(e for e in pub_list[0] if e.isalnum()).lower()+".txt"
            fil_pat = "./data/" + dir_mon + "/" + fil_nam
            print("<h2>events: Create {0} </h2>".format(pub_list[0]))
            with open("single.html") as event_view:
                event_view = str(event_view.read())                    
                print(event_view.format(*pub_list))
                print("<p><p>")
                events_list = []
                for root, dirnames, filenames in os.walk("./data/"):
                    for filename in filenames:
                        events_list.append(filename)
                if fil_nam in events_list:
                    print("Sorry, event exists.<p>")
                    print("<a href='?m=add'>&larr; back</a><br>")
                    print("<a href='?'>&larr; &larr; home</a>")
                    break
                else:
                    with open('preview.html', 'r') as page:
                        print(page.read().format(group_key, pub_string, fil_pat))
                print("<a href='?m=view'>&larr; events</a><br><a href='.'>&larr; &larr; home</a>")
                break
        elif pb_status:
            print(pb_status)
            break

        elif row_modded == 1:
            array = []
            for line in lines:
                array.append(line)
            guest_name = escape_html(guest_name.replace(",", "-"))
            array[6] = ", ".join((array[6], guest_name))
            array.append('')
            with open(event_fil, 'w') as db2:
                db2.write("\n".join(array))
            print("You've joined <i>", array[0], "</i> succesfully,",  \
              guest_name +"!")
            print('<p><a href="?m=view;v=' + event_name + '">')
            print('&larr; back</a>')
            print('<br><a href="?m=view">&larr; &larr; events</a>')
            print('<br><a href="?">&larr; &larr; &larr; home</a>')
            break

def single_event_view(event_name, group_key=""):
    for root, dirnames, filenames in os.walk("./data/"):
        for filename in filenames:
            if event_name == filename[:-4]:
                with open(os.path.join(root, filename)) as ur_event:
                    lines = ur_event.read().splitlines()
                    print("<h2>events: "+lines[0]+"</h2>")
                    if lines[1][0] == "0" or str(lines[1][2:]) == group_key:
                        event_table = [lines[0], lines[2], lines[3],
                        markdown(lines[4]), "", lines[5], "", \
                                       lines[6], ""]
                        event_table[4] = lines[6].split(", ")[0]
                        event_table[-1] = str(len(lines[6].split(", ")))
                        with open("single.html") as event_view:
                            event_view = str(event_view.read())
                            print(event_view.format(*event_table))
                        with open("join.html") as event_joiner:
                            event_joiner = str(event_joiner.read())
                            print("<p>", event_joiner.format(filename[:-4]))
                        print("<hr>")
                        form = cgi.FieldStorage()
                        ctext = form.getvalue('ctext')
                        cname = form.getvalue('cname')
                        stamp = form.getvalue('stamp')
                        if (len(lines) - 7) != 1:
                            print('<i> {0} comments </i><p>'.format(len(lines) - 7))
                        else:
                            print('<i> {0} comment</i><p>'.format(len(lines) -7))
                        if not ctext:
                            if (len(lines) - 7) > 0:
                                print('<table border="1px" style="border-collapse:collapse;width:350px;">')
                                cntr = 0
                                for line in lines[7:]:
                                    if line != "":
                                        cntr += 1

                                        line = line.split("|")
                                        print("""<tr style="background-color:#ccc"><td style="max-width: 5%;">{3}.
<td>Name: {0}</td>
<td>@ {1} 
<tr><td colspan="3" style="max-width:350px; word-wrap:break-word">{2}<p>
""".format(line[0][:13], line[1], line[2], str(cntr)))
                                print("</table><p>")
                            with open("comments.html", "r") as page:
                                print(page.read().format(event_name, group_key))
                        else:
                            ctext = escape_html(ctext)
                            cname = escape_html(cname)
                            if not stamp:
                                if not cname:
                                    cname = "Anonymous"
                                now = datetime.datetime.now()
                                now = now.strftime("%b %d %H:%M")
                                with open('previewcomment.html', 'r') as page:
                                    print(page.read().format(event_name, cname[:14], ctext, now, group_key))
                            else:
                                stamp = escape_html(stamp)
                                print("<a href='?m=view;v={0};k={1}'>&larr; go back</a>".format(event_name, group_key))
                                print("<p> Comment posted!")
                                print("<hr>")
                                with open(os.path.join(root, filename), "a") as event:
                                    event.write("|".join((cname, stamp, ctext+"\n")))
                        print("<a href='?m=view'>&larr; events</a><br><a href='.'>&larr; &larr; home</a>")
                    else:
                        print('<div style="text-align:center; margins: 0 0 auto; width: 160px;' + \
'border:2px solid black; padding-bottom: 5px;"><img src="lock.png"></div>')
                        if not group_key:
                            print("<br>This event requires a key to view.<p>")
                        else:
                            print(group_key)
                            print("<br>Sorry, wrong key entered.<p>")
                        print("<form method='get' action='?'>")
                        print("<input type='hidden' name='m' value='view'>")
                        print("<input type='hidden' name='v' value='" + \
                              filename[:-4] + "'>")
                        print("<input type='password' name='k'>")
                        print("<input type='submit' value='Enter'><br>")
                        print("</form>")
                        print("<a href='?m=view'>&larr; events</a>")
                        print("<br><a href='.'>&larr; &larr; home</a>")
                        break
    
def event_publish():
    form = cgi.FieldStorage()
    event_params = ['n', 't1', 't2', 't3', 'p', 'h', 'd', 'pb']
    opt_params = {'y':"Private", 'g':"Group", 'l':"Location"}
    event_details = []
    # title ; privacy:key ; date; location; details; group; host
    if form.getvalue('n'):
        event_details.append(escape_html(form.getvalue('n')))
        if form.getvalue('y'):
            event_details.append("1:" + escape_html(form.getvalue('p')))
        else:
            event_details.append("0:" + escape_html(form.getvalue('p')))
        event_details.append(" ".join((escape_html(form.getvalue('t1')),
                              escape_html(form.getvalue('t2'))+",", \
                              escape_html(form.getvalue('t3')) + ":00")))
        if form.getvalue('l') is None:
            event_details.append("Unknown")
        else:
            event_details.append(escape_html(form.getvalue('l')))
        event_details.append(escape_html(form.getvalue('d')))
        if form.getvalue('g') is None:
            if form.getvalue('y'):
                event_details.append("Private")
            else:
                event_details.append("Public")
        else:
            event_details.append(escape_html(form.getvalue('g')))
        event_details.append(escape_html(form.getvalue('h')).replace(",", "-"))
        event_details = "|".join(event_details)

        if not form.getvalue('pb'):
            event_edit(event_params[0], event_params[5], event_details, \
                   form.getvalue('p'))
    if form.getvalue('pb') and form.getvalue('eventfn'):
        event_string = form.getvalue('pb').replace('|',"\n") + "\n"
        event_filename = escape_html(form.getvalue('eventfn'))
        with open(event_filename, 'x') as event_create:
            print("<h2>events: Publish</h2>")
            print("<p>Congratulations, ")
            print(event_string.split("\n")[-2] + \
              ". Your event has been created.<p>")
            print("""<a href="?m=view">&larr; events</a>
<br><a href=".">&larr; &larr; home</a>""")
            cal_data = event_string.split("\n")
            with open("./data/cal.list", 'a') as cal:
                cal_data[2] = months[cal_data[2][:3]] + cal_data[2][4:6] + cal_data[2][7:]
                cal.write("|".join(["\n"+cal_data[2], cal_data[0], cal_data[1][0], cal_data[6]]))
            event_create.write(event_string)
        
def create_event():
    form = cgi.FieldStorage()
    event_params = ['n', 't1', 't2', 't3', 'p', 'h', 'd', 'event']
    for params in event_params:
        params = escape_html(params)
    event_name = form.getvalue('n')
    event_params[6] = '<br>'.join(event_params[6].split(r'\r'))
    if event_name:
        print("<form action='./?m=publish'>")
        for param in event_params:
            print("<br>"+param+": "+str(form.getvalue(param)))
        print("<br>")
        group_setting = form.getvalue('g')
        secret_mode = form.getvalue('y')
        event_location = form.getvalue('l')
        if secret_mode and group_setting is None:
            group_setting = "Private"
        if group_setting is None:
            group_setting = "Public"
        if secret_mode:
            print("<br>Private: yes")
        if event_location is None:
            event_location = "Unknown"
        print("<br>Group: ", group_setting,"")
        if event_location:
            print("<br>Location: ", event_location) 
        print("""<br><form action='?m=publish'>
<input value='dummy' type='submit'></form><br>""")
    else:
        print("<h2>events: Create event</h2>")
        if form.getvalue('p'):
            print("Your password is:", form.getvalue('p'))
        with open("create.html") as createvent:
            print(createvent.read())

def event_calendar(munth=''):
    if munth == '':
        munth = time.strftime("%m")
    if len(munth) < 2:
        munth = "0" + munth
    print("<h2>events: Calendar</h2>")
    calendar.setfirstweekday(6)
    cal_list = []
    with open("./data/cal.list") as cal_events:
        lines = cal_events.read().splitlines()
        lines = sorted(lines)
        for line in lines:
            line = line.split("|")
            if line[0][:2] == str(munth):
                linky = ''.join(e for e in line[1] if e.isalnum()).lower()
                cal_list.append([line[0][2:4], line[1], linky, line[2]])
#    print(cal_list)
    cal_day = cgi.FieldStorage().getvalue('d')
    day_mode = None
    for eve in cal_list:
        if eve[0] == cal_day:
            day_mode = 1

    print("<table style='border: black 2px solid; \
            border-collapse: collapse; text-align:center'>")
    print("<tr style='height: 2em'>")
    print("<td style='background-color: #999'>")
    print("<a href='?m=cal;")
    if munth != "01":
        print("mon={0}'>".format(str(int(munth)-1)))
    else:
        print("mon=12'>")
    print("&#171</a>")
    print("<td colspan='5' style='background-color: #bbb'>")
    print(str(year) + "-" + str(munth))
    print("<td style='background-color: #999'>")
    print("<a href='?m=cal;")
    if munth != "12":
        print("mon={0}'>".format(str(int(munth)+1)))
    else:
        print("mon=1'>")
    print("&#187;</a>")
    cal_days = []
    for day in calendar.Calendar(6).itermonthdays(year, int(munth)):
        cal_days.append(day)
    cal_dayc = len(cal_days)
    weak_days = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
    print("<tr>")
    for days in weak_days:
        print("<td class='day'>{0}</td>".format(days))
    print("</tr><tr>")
    for day in cal_days:
        if cal_dayc % 7 == 0:
            print("<tr>")
        if day == 0:
            print("<td class='null'> -")
        else:            
            for dayz in cal_list:
                try:
                    if day[0] == int(dayz[0]):
                        day[1] += "!"
                except:
                    if day == int(dayz[0]):
                        day = [day, "!"]
            try:
                if len(day[1]) >= 2:
                    if day_mode:
                        if int(day[0]) != int(cal_day):
                            print("<td style='background-color:#e8e8e8'>", day[0])
                        else:
                            print("<td class='multi'>",
                                  "<a href='?m=cal;mon={0}'>".format(munth),
                                  day[0], "</a>")
                    else:
                        print("<td class='multi'>")
                        if len(str(day[0])) == 1:
                            day[0] = "0" + str(day[0])
                        print("<a href='?m=cal;mon={0};d={1}'>".format(munth, day[0]))
                        print(int(day[0]), "</a>")
                            
                else:
                    if day_mode:
                        print("<td class='boring'>", day[0])
                    else:
                        for event in cal_list:
                            if int(event[0]) == int(day[0]):
                                if event[3] == "1":
                                    print("<td class='priv'>")
                                else:
                                    print("<td class='pub'>")
                                print("<a href='?m=view;v={0}'>{1}</a>".format(event[2], day[0]))
                
                                
            except:
                print("<td class='boring'>")
                print(day)
        cal_dayc += -1                
    print("</tr></table><p>")
    num_events = str(len(cal_list))
    if day_mode == 1:
        print("""<form action="?">
<input type="hidden" name="m" value="cal">
<input type="hidden" name="mon" value="{0}">
<input type="submit" value="Show more">
</form>""".format(munth))
        num_events = []
        for e_i in cal_list:
            if e_i[0] == cal_day:
                num_events.append(e_i)
    if num_events != "0":
        bloop = "events:"
        if cal_day and day_mode:
            num_events = str(len(num_events))
            num_events = munth + "-" + cal_day + ": " + num_events
            bloop = "events"

        print("<p><table style='border: black 2px solid; border-collapse: collapse'>")
        print("<td colspan='3' style='text-align:center; height: 2em;",
		      "background-color:#bbb'>{0} {1}".format(num_events, bloop))
    for e_i in cal_list:
        print("<tr>")
        if e_i[3] == "1":
            if day_mode and e_i[0] != str(cal_day):
                pass
            else:
                print("<td class='priv'>")
                print("&#x1f512;<td>{0}".format(munth + "-" + e_i[0]))
                print('<td><a href="?m=view;v={0}">{1}</a>'.format(e_i[2], e_i[1]))
        else:
            if day_mode == 1 and e_i[0] != str(cal_day):
                pass
            else:
                print("<td class='pub'>")
                print("&#127758;<td>{0}".format(munth + "-" + e_i[0]))
                print('<td><a href="?m=view;v={0}">{1}</a>'.format(e_i[2], e_i[1]))
    if num_events:
        print("</table>")
    print("<p> <a href='.'>&larr; home</a>")


def join_event(event_title, guest_name):
    print(event_title, guest_name)

def main():
    form = cgi.FieldStorage()
    page_mode = form.getvalue('m')
    view_event = form.getvalue('v')
    group_key = form.getvalue('k')
    guest_name = form.getvalue('name')
    pb_status = form.getvalue('pb')
    event_filename = form.getvalue('eventfn')
    print("Content-type: text/html\r\n")	
    with open("head.html") as header:
        print(header.read())
    print("<center><meta name=viewport content='width=600px'>")
    if page_mode:
        if page_mode == "view":
            if view_event:
                single_event_view(view_event, group_key)
            else:
                events_view(group_key)
                print("<br><a href='.'>&larr; home</a>")
        elif page_mode == "add":
            create_event()
            print("<br><a href='.'>&larr; home</a>")
        elif page_mode == "publish":
            event_publish()
        elif page_mode == "join":
            event_edit(view_event, guest_name)
        elif page_mode == "cal":
            if form.getvalue('mon'):
                event_calendar(form.getvalue('mon'))
            else:
                event_calendar()
        else:
            print("<p><a href='.'>clear mode</a><p>")
            
    else:
        with open("welcome.html") as w:
            print(w.read())

main()
