

#!/usr/bin/perl
# --
# otrs.SOAPRequest.pl - sample to send a SOAP request to OTRS Generic Interface Ticket Connector
# Copyright (C) 2001-2013 OTRS AG, http://otrs.com/
# --
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU AFFERO General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
# or see http://www.gnu.org/licenses/agpl.txt.
# --

use strict;
use warnings;

#use ../ as lib location
use File::Basename;
use FindBin qw($RealBin);
use lib dirname($RealBin);

use SOAP::Lite;
use Data::Dumper;
	
# ---
# Variables to be defined

# 
my $Operation = 'TicketUpdate';

my $TicketNumber = $ARGV[0];#'2016082662000041';
my $username = $ARGV[1];#'root@localhost';
my $password = $ARGV[2];#'pass@word1';
my $IP=$ARGV[3];
my $ORACLEServer=$ARGV[4];
my $ORACLESeUsername=$ARGV[5];
my $OraHome12=$ARGV[6];
my $OraHome11=$ARGV[7];
my $TNSList=$ARGV[8];
my $DBName=$ARGV[9];



;#'192.168.255.169'
#this is the URL for the web service
# the format is
# <HTTP_TYPE>:://<OTRS_FQDN>/nph-genericinterface.pl/Webservice/<WEB_SERVICE_NAME>
# or
# <HTTP_TYPE>:://<OTRS_FQDN>/nph-genericinterface.pl/WebserviceID/<WEB_SERVICE_ID> 
my $URL ='http://'.$IP.'/otrs/nph-genericinterface.pl/Webservice/GenericTicketConnector';
# this name space should match the specified name space in the SOAP transport for the web service
my $NameSpace = 'http://www.otrs.org/TicketConnector/';

# this is operation to execute, it could be TicketCreate, TicketUpdate, TicketGet, TicketSearch
# or SessionCreate. and they must to be defined in the web service.

# this variable is used to store all the parameters to be included on a request in XML format, each
# operation has a determined set of mandatory and non mandatory parameters to work correctly, please
# check OTRS Admin Manual in order to get the complete list
my $sub="Oracle Upgradation- Initiated";

# this variable is used to store all the parameters to be included on a request in XML format, each
# operation has a determined set of mandatory and non mandatory parameters to work correctly, please
# check OTRS Admin Manual in order to get the complete list
if (@ARGV == 10)
{
my	$hcon="<!DOCTYPE html><html lang=\"en\"><body><p>Hi Team,</p><p>This is to inform that  the ORACLE Upgradation process is been initiated</p><p>Also find the <b> Input Details </b> for this process...</p><table align=\"left\" border=\"1\" cellpadding=\"1\" cellspacing=\"1\" dir=\"ltr\" style=\"width:60%;\">    <thead>    <tr>        <th scope=\"col\" style=\"text-align: left; vertical-align: middle; background-color: rgb(0, 51, 102);\"><span style=\"color:#FFFFFF;\">Components</span></th><th scope=\"col\" style=\"text-align: left; vertical-align: middle; background-color: rgb(0, 0, 102);width: 60%;\"><span style=\"color:#FFFFFF;\">Values</span></th></tr></thead><tbody>
	<tr><td>Server IP or Hostname</td><td>$ORACLEServer</td></tr><tr><td colspan=\"2\" ><span style=\"color:#808000;\"><b>UPGRADATION Details</b></td></tr>
 <tr>
                <td> Oracle Installer Username</td>
                <td>$ORACLESeUsername</td>
            </tr>
			<tr><td colspan=\"2\"><span style=\"color:#808000;\"><b>Upgradation Details</b></td></tr><tr>
			<tr>
                <td> Oracle Home (11.2.0.4)</td>
                <td>$OraHome11</td>
            </tr>
						 <tr>
                <td> Oracle Home (12.1.0.2)</td>
                <td>$OraHome12</td>
            </tr>
			<tr>
                <td> TNS List</td>
                <td>$TNSList</td>
            </tr>
			<tr>
                <td> Upgrade will be performed on</td>
                <td>$DBName</td>
            </tr>";
		
	$hcon=$hcon."</tbody></table><br><br><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p><br><br><br><br><br><p>Thanks &amp; Regards,</p><p>SS Automation Team</p><p>ssauto\@capgemini.com</p></body></html>";
	my $con="<![CDATA[$hcon]]>";
	my $XMLData = "
	<UserLogin>$username</UserLogin>
	<Password>$password</Password>
	<TicketNumber>$TicketNumber</TicketNumber>
	<Ticket>
		<Title>In progress</Title>
		<State>In Progress</State>   
	</Ticket>
	<Article>
		 <Subject>$sub</Subject>
		 <Body>$con</Body>
		 <ContentType>text/html; charset=utf8</ContentType>
	 </Article>
	";

	# ---

	# create a SOAP::Lite data structure from the provided XML data structure
	my $SOAPData = SOAP::Data
		->type( 'xml' => $XMLData );

	my $SOAPObject = SOAP::Lite
		->uri($NameSpace)
		->proxy($URL)
		->$Operation($SOAPData);

	# check for a fault in the soap code
	if ( $SOAPObject->fault() ) {
	print "1\n";
	print "ExitDesc: Ticket Updation Failed\n";
	print $SOAPObject->faultcode(), " ", $SOAPObject->faultstring(), "\n";
	}

	# otherwise print the results
	else {

		# get the XML response part from the SOAP message
		my $XMLResponse = $SOAPObject->context()->transport()->proxy()->http_response()->content();

		# deserialize response (convert it into a perl structure)
		my $Deserialized = eval {
			SOAP::Deserializer->deserialize($XMLResponse);
		};

		# remove all the headers and other not needed parts of the SOAP message
		my $Body = $Deserialized->body();

		# just output relevant data and no the operation name key (like TicketCreateResponse)
		for my $ResponseKey ( sort keys %{$Body} ) {
		print "0\n";
		print "ExitDesc: Ticket Updated Successfully\n";

		print Dumper( $Body->{$ResponseKey} );    ## no critic
		}
	}
}
else
{
	print "10\n";
	print "Missing Arguments\n";
}