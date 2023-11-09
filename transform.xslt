<?xml version="1.0" encoding="UTF-8" ?>
<?xml-stylesheet type="text/xsl" href="transform.xslt"?>

<xsl:stylesheet version="2.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:xs="http://www.w3.org/2001/XMLSchema">
<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
    <!-- Define the transformation rules -->
    <xsl:template match="/">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <meta charset="utf-8"/>
            <title>STIB realtime - Stockel</title>
            <link rel="apple-touch-icon" type="svg" href="https://www.stib-mivb.be/irj/go/km/docs/WEBSITE_RES/Webresources/Frontend/build/images/logo--mobile.svg" class="next-head"/>
            <link rel="icon" type="svg" href="https://www.stib-mivb.be/irj/go/km/docs/WEBSITE_RES/Webresources/Frontend/build/images/logo--mobile.svg" class="next-head"/>
            <link rel="icon" type="svg" href="https://www.stib-mivb.be/irj/go/km/docs/WEBSITE_RES/Webresources/Frontend/build/images/logo--mobile.svg" class="next-head"/>
            <meta name="description" content=""/>
            <meta name="viewport" content="width=device-width, initial-scale=1"/>

            <meta property="og:title" content=""/>
            <meta property="og:type" content=""/>
            <meta property="og:url" content=""/>
            <meta property="og:image" content=""/>

            <link rel="manifest" href="site.webmanifest"/>
            <link rel="apple-touch-icon" href="icon.png"/>
            <!-- Place favicon.ico in the root directory -->

            <link rel="stylesheet" href="css/main.css"/>

            <meta name="theme-color" content="#fafafa"/>
            <script src="js/main.js"></script>

            <!-- Refresh the page automaticaly -->
            <meta http-equiv="refresh" content="10"/>
        </head>
        <body>
            <h2>STIB realtime - Stockel</h2>
            <table>
                <xsl:for-each select="data/records/fields/passingtimes/vehicle">
                    <tr>
                        <xsl:attribute name="id">
                            <xsl:text></xsl:text>
                            <xsl:value-of select="@vehicle_number"/>
                        </xsl:attribute>
                        <xsl:if test="./message/@fr">
                            <xsl:attribute name="class">
                                <xsl:text>message</xsl:text>
                            </xsl:attribute>
                        </xsl:if>
                        <td>
                            <div class="lines">
                                <div>
                                    <xsl:attribute name="class">
                                        <xsl:text>line line-</xsl:text>
                                        <xsl:value-of select="./lineId/@id"/> <!-- Access and output the "id" attribute of lineId -->
                                    </xsl:attribute>
                                    <span>
                                        <xsl:value-of select="./lineId/@id"/> <!-- Access and output the "id" attribute of lineId -->
                                    </span>
                                </div>
                                <h1 class="direction">
                                    <xsl:value-of select="./destination/@fr"/> <!-- Access and output the "fr" attribute of destination -->
                                </h1>
                            </div>
                        </td>
                        <td>
                            <p class="lefttime"><xsl:value-of select="./expectedArrivalTime"/></p>
                        </td>
                    </tr>
                    <xsl:if test="./message/@fr">
                        <tr>
                            <td colspan="2">
                                <div class="alert alert-danger"><xsl:value-of select="./message/@fr"/></div>
                            </td>
                        </tr>
                    </xsl:if>
                </xsl:for-each>
            </table>
            
        </body>
        </html>
    </xsl:template>

</xsl:stylesheet>