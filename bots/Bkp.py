# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import pyodbc
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount


class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
                
    async def on_message_activity(self, turn_context: TurnContext):

        name = turn_context.activity.from_property.name
        return await turn_context.send_activity(
            f"Welcome {name}"
        )



    async def on_message_activity(self, turn_context: TurnContext):
        """DRG <Request ID> :Returns status of DRG/DRM Requests"""
        url = "http://uls-win-drmprod.hgst.com/drm-web-client/m/go.aspx/Cloud%20Prod/request/"
        con = pypyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};Server=ULS-SQL02-SQL01.HITACHIGST.GLOBAL,57013;Database=EDM_CLOUD;uid=edm_cloud_ro_svc;pwd=3Pw_10D17#')
        
        # MSSQL database format
        cursor = con.cursor()
        con.timeout = 60

        """Status command format should be: "status x(id)
        local variable query_string takes args
        argument(request id) is a string of numbers i.e. 111 ranging from 3-4 digits"""
        
        # curDate = datetime.now()
        db = pypyodbc.connect(
            'Driver={ODBC Driver 17 for SQL Server};Server=ULS-SQL02-SQL01.HITACHIGST.GLOBAL,57013;Database=EDM_DRM_JABBER;uid=EDM_DRM_Write;pwd=m0E_6dW#')
        
        dbcursor = db.cursor()
        sql = "insert into DRG_JabberBot VALUES('%s', '%s', '%s')" % (usrName, drgID, str(datetime.datetime.now()))
        dbcursor.execute(sql)
        db.commit()

        if args == '':
            return 'Missing argument: Request ID'

        else:
            if not args.isdigit():
                return "ID must be numeric"
            req_id = int(args)
            try:

                # most recent activity id
                cursor.execute("""SELECT RM_WF_Request_Activity.i_workflow_request_id, RM_WF_Request.e_workflow_status__current, RM_WF_Request_Activity.c_stage_name, CASE WHEN [RM_WF_Request].[e_workflow_status__current] <> 'Committed' THEN DATEDIFF(DD, RM_WF_Request_Stage.d_started_on, GETDATE()) ELSE 0 END AS Age,
                           RM_WF_Request_Assigned_To.c_name, COALESCE (RM_User.c_user_name + ', ', '') AS userName
                           FROM RM_WF_Request_Activity LEFT OUTER JOIN
                           RM_WF_Request_Assigned_To ON RM_WF_Request_Activity.i_workflow_request_id = RM_WF_Request_Assigned_To.i_workflow_request_id INNER JOIN
                           RM_WF_Request ON RM_WF_Request_Activity.i_workflow_request_id = RM_WF_Request.i_workflow_request_id INNER JOIN
                           RM_WF_Request_Stage ON RM_WF_Request.i_workflow_request_id = RM_WF_Request_Stage.i_workflow_request_id AND RM_WF_Request.i_current_stage_id = RM_WF_Request_Stage.i_model_stage_id LEFT OUTER JOIN
                           RM_Access_Group_Definition ON RM_Access_Group_Definition.c_abbrev = RM_WF_Request_Assigned_To.c_name LEFT OUTER JOIN
                           RM_Access_Group_User ON RM_Access_Group_Definition.i_security_id = RM_Access_Group_User.i_security_id LEFT OUTER JOIN
                           RM_User ON RM_Access_Group_User.i_user_id = RM_User.i_user_id
                           WHERE  (RM_User.c_user_name NOT IN ('ADMIN','BatchAdmin', 'Neha.Gahtori2@wdc.com', 'Pranab.Dash@wdc.com','adrian.cuyugan@wdc.com' ) or RM_User.c_user_name IS NULL) and   RM_WF_Request_Activity.i_activity_id = (SELECT  MAX(i_activity_id) AS Expr1
                               FROM   RM_WF_Request_Activity AS RM_WF_Request_Activity_1
                               WHERE  (i_workflow_request_id = ?));""", [req_id])
                if cursor.rowcount == 0:
                    return 'Request ID does not exist'
                row = cursor.fetchone()
                rstr = ""
                if (row[4] == None):
                    return (
                               """<body><strong>Request ID:</strong> <a href="%s"> %s </a> \n<strong>Status:</strong> %s \n<strong>Stage:</strong> %s \n<strong>Stage Age:</strong> %s Days \n<strong>Assigned to Group:</strong> N/A</body>""") % (
                               url + str(row[0]), row[0], row[1], str(row[2].replace('&', '&amp;')), row[3])
                else:
                    rstr += (
                                """<body><strong>Request ID:</strong> <a href="%s"> %s </a> \n<strong>Status:</strong> %s \n<strong>Stage:</strong> %s \n<strong>Stage Age:</strong> %s Days \n<strong>Assigned to Group:</strong> %s \n<strong>Assigned to Users:</strong> \n      <font color="blue">%s</font>""") % (
                                url + str(row[0]), row[0], row[1], str(row[2].replace('&', '&amp;')), row[3],
                                (row[4]).split('_', 1)[-1], row[5])
                    for rows in cursor.fetchall():
                        rstr += """ \n      <font color="blue">%s</font>""" % (rows[5])

                #return rstr + "</body>"

                return await turn_context.send_activity({rstr + "</body>"}
       
            #con.commit()
            #dbcursor.close()
            #db.close()
           # cursor.close()
            #con.close()
