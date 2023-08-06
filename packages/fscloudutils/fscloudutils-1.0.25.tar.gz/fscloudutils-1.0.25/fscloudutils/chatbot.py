import boto3
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import requests
import json


class EmailMessanger:
    graph_template = template = (''
                                 '<a href="{graph_url}" target="_blank">'  # Open the interactive graph when you click on the image
                                 '<img src="{graph_url}.png">'  # Use the ".png" magic url so that the latest, most-up-to-date image is included
                                 '</a>'
                                 '{caption}'  # Optional caption to include below the graph
                                 '<br>'  # Line break
                                 '<a href="{graph_url}" style="color: rgb(190,190,190); text-decoration: none; font-weight: 200;" target="_blank">'
                                 'Click to comment and see the interactive graph'  # Direct readers to Plotly for commenting, interactive graph
                                 '</a>'
                                 '<br>'
                                 '<hr>'  # horizontal line
                                 '')

    def __init__(self):
        pass

    def email_template(self, sender, recipients, aws_region, subject, body, body_html):  # recipient = [list of emails]
        """
        template for e-mail sending using SES services
        :param sender: sending address
        :param recipients: list of recipients
        :param aws_region: the region specified in settings.py
        :param subject: email title
        :param body: message body
        :param body_html: message body in html regex format
        :return: None
        """
        # Replace sender@example.com with your "From" address.
        # This address must be verified with Amazon SES.
        SENDER = sender

        # Replace recipient@example.com with a "To" address. If your account
        # is still in the sandbox, this address must be verified.
        RECIPIENTS = recipients

        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        # CONFIGURATION_SET = conf_set

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        AWS_REGION = aws_region

        # The subject line for the email.
        SUBJECT = subject

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("%s\r\n"
                     "%s" % (subject, body)
                     )

        # The HTML body of the email.
        BODY_HTML = body_html

        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name=AWS_REGION)

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses':
                        RECIPIENTS,
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
                # If you are not using a configuration set, comment or delete the
                # following line
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

    def send_failure_list(self, failed_dict):
        """
        *****CURRENTLY NOT IN USE*****
        sending a list of failed failed images
        :param failed_dict: {name of the file : reason of failure}
        :return: None
        """
        BODY_HTML = """<html>
            <head></head>
            <body>
              <h1>Amazon SES Test(SDK for Python)</h1>
              <p>This email was sent with
                <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
                <a href='https://aws.amazon.com/sdk-for-python/'>
                  AWS SDK for Python (Boto)</a>.</p>
            </body>
            </html>
                        """

    def send_download_links(self, url, region_name, project_name, summary, sender, recipients):
        """
        by using email_template function, the following method creates a message template using an preassigned url.
        :param url: a url address to the file on S3
        :param region_name: name of the region as it specified in settings.py
        :param project_name: name of the project
        :return: None
        """
        sender = sender
        recipients = recipients
        subject = "%s results" % project_name
        body = url
        body_html = """<html>
                <head></head>
                <body>
                  <h1>%s are ready for download, the link will be valid for the next 12h:</h1>
                  <a href=%s>%s</a>
                  <h1>Output files Validation result:  </h1>
                  <p>%s</p>
                </body>
                </html>
                            """ % (subject, url, url, summary)

        self.email_template(sender, recipients, region_name, subject, body, body_html)

    def send_calibration_file(self, region_name, plot_name, project_name, calibration_file_path, sender, recipients):
        """
        sending the calibration file using raw email form
        :param region_name: the region as it specified in settings.py
        :param plot_name: name of the plot
        :param project_name: name of the project
        :param file: the path to the 'calibration.csv' file
        :param sender: a sender email address
        :param recipients: list of recipients
        :return:
        """
        # make path string
        try:
            str_path = str(calibration_file_path)
        except:
            str_path = None
        # define message parameters
        message = MIMEMultipart('mixed')
        message['Subject'] = 'Calibration for %s on project %s' % (plot_name, project_name)
        message['From'] = sender
        message['To'] = ', '.join(recipients)

        # Message body
        BODY_HTML = """\
        <html>
        <head></head>
        <body>
        <h1>Hello!</h1>
        <p>Please see the attached calibration file.</p>
        </body>
        </html>
        """
        htmlpart = MIMEText(BODY_HTML.encode("utf-8"), 'html', "utf-8")
        message.attach(htmlpart)

        try:
            # Attachment
            part = MIMEApplication(open(str_path, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=calibration_file_path.parts[-1])
            message.attach(part)
        except:
            print("No calibration file sent...")

        # Send
        client = boto3.client('ses', region_name=region_name)
        try:
            response = client.send_raw_email(
                Source=message['From'],
                Destinations=recipients,
                RawMessage={
                    'Data': message.as_string()
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

    def send_color_dist(self, region_name, plot_name, color_data_file_path, graph1, graph2, sender, recipients):
        """
        sending the color distribution file and graph using raw email form
        :param region_name: the region as it specified in settings.py
        :param plot_name: name of the plot
        :param project_name: name of the project
        :param file: the path to the 'calibration.csv' file
        :return:
        """
        # make path string
        str_path = str(color_data_file_path)
        # define message parameters
        message = MIMEMultipart('mixed')
        message['Subject'] = 'Color distribution for %s' % (plot_name)
        message['From'] = sender
        message['To'] = ', '.join(recipients)

        # Message body
        BODY_HTML = """\
        <html>
        <head></head>
        <body>
        <h1>Hello!</h1>
        <p>Please see the attached graph and data file.</p>
        </body>
        </html>
        """
        htmlpart = MIMEText(BODY_HTML.encode("utf-8"), 'html', "utf-8")
        message.attach(htmlpart)

        # Attachment of file
        part = MIMEApplication(open(str_path, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename="%s_color_distribution_data.xlsx" % plot_name)
        message.attach(part)

        # Attachment of graph 1
        part = MIMEApplication(open(graph1, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=graph1)
        message.attach(part)

        # Attachment of graph 2
        part = MIMEApplication(open(graph2, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=graph2)
        message.attach(part)

        # Send
        client = boto3.client('ses', region_name=region_name)
        try:
            response = client.send_raw_email(
                Source=message['From'],
                Destinations=recipients,
                RawMessage={
                    'Data': message.as_string()
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])


class SlackMessanger:
    def __init__(self, slack_token: str, slack_channel: str):
        self.slack_token = slack_token
        self.slack_channel = slack_channel
        self.slack_icon_emoji = ':beer:'
        self.slack_user_name = 'Beer'

    def parse_ssm_file(self, error_log_url: str):
        try:
            with open('/tmp/ssm.txt', 'r') as f:
                for line in f.readlines():
                    if "APP_METHOD" in line:
                        self.app_method = line.split("=")[1].replace("\n", "")
                    elif "INSTANCE_TYPE" in line:
                        self.instance_type = line.split("=")[1].replace("\n", "")
                    elif "DEFAULT_BUCKET" in line:
                        self.environment = line.split("-")[1].upper()
        except FileNotFoundError as err:
            self.app_method = "UNKNOWN-METHOD"
            self.instance_type = "UNKNOWN-TYPE"
            self.environment = "STAGE"

        self.log_url = error_log_url.format(self.environment, self.instance_type, self.app_method, self.block_name)

    def post_message_to_slack(self, message: str, blocks: list = None):
        return requests.post('https://slack.com/api/chat.postMessage', {
            'token': self.slack_token,
            'channel': self.slack_channel,
            'text': message,
            'icon_emoji': self.slack_icon_emoji,
            'username': self.slack_user_name,
            'blocks': json.dumps(blocks) if blocks else None
        }).json()

    def post_file_to_slack(self, text: str, file_name: str, file_bytes, file_type=None, title=None):
        return requests.post(
            'https://slack.com/api/files.upload',
            {
                'token': self.slack_token,
                'filename': file_name,
                'channels': self.slack_channel,
                'filetype': file_type,
                'initial_comment': text,
                'title': title
            },
            files={'file': file_bytes}).json()

    def generate_error_message(self, title: str, description: str):
        return f"An error has occurred with {title}:\n{description}"