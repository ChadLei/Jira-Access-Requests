# -*- coding: utf-8 -*-
import smtplib
import emoji

def completion_email(username, ticket_number, request_type):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        server.starttls()
        server.login('chad.lei@perficient.com', 'Ilovegreentea4!')
        server.ehlo()

        # Email content information
        FROM = "chad.lei@perficient.com"
        TO = ['cblei@uci.edu']
        SUBJECT = "Ticket completed: %s %s" % (ticket_number, request_type)
        TEXT = '''Hey buddy, here's the information you're looking for: \r\n
        Crowd User: https://crowd.ngptools.com/crowd/console/secure/user/view!execute.action?name=%s&directoryID=8454145\r\n
        Jira Ticket: https://issues.ngptools.com/jira/browse/%s\r\n\n
        ''' % (username, ticket_number)

        # Preparing the message format
        message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

        %s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        # Send the message
        server.sendmail(FROM, TO, message)
        print '---- Completion-email sent! ----'
        print emoji.emojize(":thumbs_up:") + emoji.emojize(":thumbs_up:") + " Ticket completed! " + emoji.emojize(":thumbs_up:") + emoji.emojize(":thumbs_up:")
        server.quit()

    except smtplib.SMTPAuthenticationError as e:
        print 'Authentication error: ' + str(e)
    except:
        print 'Something went wrong - try again.'

def panic_email(username, ticket_number, request_type):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        server.starttls()
        server.login('chad.lei@perficient.com', 'Ilovegreentea4!')
        server.ehlo()

        # Email content information
        FROM = "chad.lei@perficient.com"
        TO = ['cblei@uci.edu']
        SUBJECT = "Attention Required: %s %s" % (ticket_number, request_type)
        TEXT = '''Hey buddy, here's the information you're looking for: \r\n
        Crowd User: https://crowd.ngptools.com/crowd/console/secure/user/view!execute.action?name=%s&directoryID=8454145\r\n
        Jira Ticket: https://issues.ngptools.com/jira/browse/%s\r\n\n
        ''' % (username, ticket_number)

        # Preparing the message format
        message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

        %s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        # Send the message
        server.sendmail(FROM, TO, message)
        print '---- Failed-email sent! ----'
        server.quit()

    except smtplib.SMTPAuthenticationError as e:
        print 'Authentication error: ' + str(e)
    except:
        print 'Something went wrong - try again.'

def send_email(username, email):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        server.starttls()
        server.login('chad.lei@perficient.com', 'Ilovegreentea4!')
        server.ehlo()
        print 'Finalizing ticket completion ....'

        # Email content information
        FROM = "chad.lei@perficient.com"
        TO = [email]
        SUBJECT = "Your User Name to access the FordDirect Collaboration Tools (JIRA & WIKI)"
        TEXT = '''Welcome to NGPTools, the Collaborative Toolset we use at FordDirect. Your User Name is:\r\n
        %s\r\n\n
        The NGPTools landing page is here: http://issues.ngptools.com/ & from there you can navigate to the applications you need.\r\n
        Your password is required to be changed every 90 days.\r\n
        • Password Change URL:https://crowd.ngptools.com/crowd/console/forgottenlogindetails!execute.action\r\n\n
        Enjoy NGPTools!
        ''' % (username)

        # Preparing the message format
        message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

        %s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        # Send the message
        server.sendmail(FROM, TO, message)
        print '---- Email sent to user! ----'
        # print emoji.emojize(":thumbs_up:") + emoji.emojize(":thumbs_up:") + " Ticket completed! " + emoji.emojize(":thumbs_up:") + emoji.emojize(":thumbs_up:")
        server.quit()

    except smtplib.SMTPAuthenticationError as e:
        print 'Authentication error: ' + str(e)
    except:
        print 'Something went wrong - try again.'



if __name__ == '__main__':
    send_email('lisamathey', 'Lisa.Mathey@vml.com')
