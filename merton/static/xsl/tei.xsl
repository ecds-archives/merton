<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0"
		xmlns:exist="http://exist.sourceforge.net/NS/exist"
               version="1.0">

  <xsl:variable name="figure-path">/static/images/pages/</xsl:variable>
  <xsl:variable name="figure-suffix">.jpg</xsl:variable>
  <xsl:variable name="thumbnail-path">http://beck.library.emory.edu/frenchrevolution/image-content/thumbnails/</xsl:variable>
  <xsl:variable name="thumbnail-suffix">.gif</xsl:variable>

  <!-- ignore teiheader for now -->
  <xsl:template match="tei:teiHeader"/>

  <xsl:template match="tei:div">
    <div>
      <xsl:attribute name="class"><xsl:value-of select="@type"/></xsl:attribute>
     <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="tei:head">
    <p class="head"><xsl:apply-templates/></p>
  </xsl:template>

  <xsl:template match="exist:match">
    <span class="highlight"><xsl:apply-templates/></span>
  </xsl:template>

  <xsl:template match="tei:byline">
    <p class="byline"><xsl:apply-templates/></p>   
  </xsl:template>

  <xsl:template match="tei:dateline"/>

  <xsl:template match="tei:p|tei:sp">
    <p><xsl:apply-templates/></p>
  </xsl:template>
  
  <xsl:template match="tei:ref[string-length(text()) > 0]">
  	<a>
  		<xsl:attribute name="href">/display/<xsl:value-of select="translate(@target, '#', '')"/></xsl:attribute>
<xsl:attribute name="target">_top</xsl:attribute>
  		<xsl:apply-templates/>
  	</a>
  </xsl:template>

  <xsl:template match="tei:lb">
    <br/>
  </xsl:template>

  <xsl:template match="tei:quote">
    <div class="quote"><xsl:apply-templates/></div>
  </xsl:template>

  <xsl:template match="tei:note[@place='inline']">
    <span class="inline-note"><xsl:apply-templates/></span>
  </xsl:template>

  <xsl:template match="tei:note[@type='trans']">
    <p class="trans"><xsl:apply-templates/></p>
  </xsl:template>

  <xsl:template match="tei:note[@type='bibliographic'] | tei:note[@xml:id] | tei:note[@resp='#editor' and not(@place='inline') and not(@type='trans')]">
    <hr></hr>
    <div class="intext_bibl"><xsl:apply-templates/></div>
  </xsl:template>

  <xsl:template match="tei:lg">
    <p class="lg"><xsl:apply-templates/></p>
  </xsl:template>

  <xsl:template match="tei:l">
    <xsl:apply-templates/><br/>
  </xsl:template>
  
  <xsl:template match="tei:title">
    <i><xsl:apply-templates/></i>
  </xsl:template>

  <xsl:template match="tei:list">
    <ul>
      <xsl:apply-templates/>
    </ul>
  </xsl:template>

  <xsl:template match="tei:item">
    <li><xsl:apply-templates/></li>
  </xsl:template>

  <xsl:template match="tei:listBibl">
    <ul class="bibl">
      <xsl:apply-templates/>
    </ul>
  </xsl:template>
  
  <xsl:template match="tei:listBibl/tei:bibl">
    <li><xsl:apply-templates/></li>
  </xsl:template>

  <xsl:template match="tei:bibl/tei:author/tei:name/tei:choice/tei:reg"/>

  <xsl:template match="tei:cit/tei:bibl/tei:author/tei:name/tei:choice/tei:sic">
<span class="bibl"><a>
<xsl:attribute name="href">/browse/author?filter=<xsl:value-of select="."/></xsl:attribute>
<xsl:apply-templates/>
</a></span>
  </xsl:template>

  <xsl:template match="tei:foreign">
    <i><xsl:apply-templates/></i>
  </xsl:template>

  <xsl:template match="tei:speaker">
    <b><xsl:apply-templates/></b>
  </xsl:template>

  <xsl:template match="tei:hi">
    <span>
      <xsl:choose>
        <xsl:when test="@rend">
          <xsl:attribute name="class"><xsl:value-of select="@rend"/></xsl:attribute>
        </xsl:when>
        <xsl:otherwise>
          <xsl:attribute name="class">hi</xsl:attribute>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates/>
    </span>
  </xsl:template>

<xsl:template match="tei:figure">
  <a>
    <xsl:attribute name="href">/imageview/<xsl:value-of select="../@xml:id"/></xsl:attribute>
    <xsl:attribute name="alt"><xsl:value-of select="normalize-space(tei:figDesc)"/></xsl:attribute>
    <xsl:attribute name="target">_blank</xsl:attribute>
    <xsl:attribute name="id">page_image</xsl:attribute>
    View Facsimile
  </a>
</xsl:template>

</xsl:stylesheet>