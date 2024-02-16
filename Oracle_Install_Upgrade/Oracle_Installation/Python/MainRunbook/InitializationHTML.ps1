
Param(
[string] $ORACLEServer,
[string] $BinPath
)





$st='<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<table align="left" border="0" cellpadding="0" cellspacing="0" style="width:650px;">
    <tbody>
    <tr>
        <th rowspan="2" style="text-align: center; width: 50px; vertical-align: middle; background-color: rgb(102, 102, 102);"><span style="color:#FFFFFF;">IT</span></th>
        <td style="text-align: center; vertical-align: middle; width: 250px; background-color: rgb(0, 153, 153);"><span style="color:#FFFFFF;">Software Service Automation</span></td>
        <td rowspan="2" style="text-align: center; vertical-align: middle; width: 200px; background-color: rgb(0, 153, 51);"><span style="color:#FFFFFF;">ORACLE UPGRADATION</span></td>
    </tr>
    <tr>
        <td style="text-align: center; vertical-align: middle; background-color: rgb(0, 153, 153);">Automate <span style="color:#FFFFFF;">IT</span>, Change <span style="color:#FFFFFF;">IT</span>, Speed <span style="color:#FFFFFF;">IT</span></td>
    </tr>
    </tbody>
</table>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p>Hi Team,</p>
<br>
<p>This is to inform that the <b>ORACLE Installation</b>process has been triggered (which is a part of Upgradation <b>as requested</b>)</p>
<br>

<p>Also find the details.</p>
<br>

<table align="left" border="1" cellpadding="1" cellspacing="1" dir="ltr" style="width:650px;">
    <thead>
    <tr>
        <th scope="col" style="text-align: left; vertical-align: middle; background-color: rgb(0, 51, 102);"><span style="color:#FFFFFF;">Action</span></th>
        <th scope="col" style="text-align: left; vertical-align: middle; background-color: rgb(0, 0, 102);"><span style="color:#FFFFFF;">Status</span></th>
    </tr>
    </thead>
    <tbody>
	<tr>
        <td> ORACLE Server</td>
        <td>'+$ORACLEServer+'</td>
    </tr>
    <tr>
        <td> Binary Path</td>
        <td>'+$BinPath+'</td>
    </tr>
	'


$fi='</tbody>
</table>
<br>


<br>
<p>&nbsp;</p>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p>&nbsp;</p>

<p>Thanks &amp; Regards,</p>

<p>SS Automation Team</p>

<p>ssauto@capgemini.com</p>

</body>
</html>'
$fina=$st+$u+$fi
$fina