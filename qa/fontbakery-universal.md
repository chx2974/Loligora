## FontBakery report

fontbakery version: 1.1.0







## Check results



<details><summary>[3] Loligora[wght].ttf</summary>
<div>
<details>
    <summary>⚠️ <b>WARN</b> Ensure variable fonts include an avar table. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#mandatory-avar-table">mandatory_avar_table</a></summary>
    <div>


> 
> Most variable fonts should include an avar table to correctly define
> axes progression rates.
> 
> For example, a weight axis from 0% to 100% doesn't map directly to 100 to 1000,
> because a 10% progression from 0% may be too much to define the 200,
> while 90% may be too little to define the 900.
> 
> If the progression rates of axes is linear, this check can be ignored.
> Fontmake will also skip adding an avar table if the progression rates
> are linear. However, it is still recommended that designers visually proof
> each instance is at the expected weight, width etc.
> 




> Original proposal: https://github.com/fonttools/fontbakery/issues/3100





* ⚠️ **WARN** <p>This variable font does not have an avar table. Most variable fonts should include an avar table to correctly define axes progression rates.</p>
 [code: missing-avar]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check there are no overlapping path segments <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#overlapping-path-segments">overlapping_path_segments</a></summary>
    <div>


> 
> Some rasterizers encounter difficulties when rendering glyphs with
> overlapping path segments.
> 
> A path segment is a section of a path defined by two on-curve points.
> When two segments share the same coordinates, they are considered
> overlapping.
> 




> Original proposal: https://github.com/google/fonts/issues/7594#issuecomment-2401909084





* ⚠️ **WARN** <p>The following glyphs have overlapping path segments:</p>
<pre><code>* cedilla (U+00B8): L&lt;&lt;164.0,-88.0&gt;--&lt;116.0,-88.0&gt;&gt; has the same coordinates as a previous segment.

* uni0327 (U+0327): L&lt;&lt;24.0,-88.0&gt;--&lt;-24.0,-88.0&gt;&gt; has the same coordinates as a previous segment.

* cedilla.case: L&lt;&lt;164.0,-88.0&gt;--&lt;116.0,-88.0&gt;&gt; has the same coordinates as a previous segment.

* uni0327.case: L&lt;&lt;24.0,-88.0&gt;--&lt;-24.0,-88.0&gt;&gt; has the same coordinates as a previous segment.

* sterling (U+00A3): L&lt;&lt;130.0,557.0&gt;--&lt;217.0,557.0&gt;&gt; has the same coordinates as a previous segment.

* yen (U+00A5): L&lt;&lt;338.0,300.0&gt;--&lt;242.0,300.0&gt;&gt; has the same coordinates as a previous segment.

* four (U+0034): L&lt;&lt;384.0,720.0&gt;--&lt;468.0,720.0&gt;&gt; has the same coordinates as a previous segment.

* two.pnum: L&lt;&lt;403.0,401.0&gt;--&lt;471.0,344.0&gt;&gt; has the same coordinates as a previous segment.

* four.pnum: L&lt;&lt;388.0,720.0&gt;--&lt;472.0,720.0&gt;&gt; has the same coordinates as a previous segment.

* two (U+0032): L&lt;&lt;399.0,401.0&gt;--&lt;467.0,344.0&gt;&gt; has the same coordinates as a previous segment.

* 89 more.
</code></pre>
<p>Use -F or --full-lists to disable shortening of long lists.</p>
 [code: overlapping-path-segments]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Does the font contain a soft hyphen? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#soft-hyphen">soft_hyphen</a></summary>
    <div>


> 
> The 'Soft Hyphen' character (codepoint 0x00AD) is used to mark
> a hyphenation possibility within a word in the absence of or
> overriding dictionary hyphenation.
> 
> It is sometimes designed empty with no width (such as a control character),
> sometimes the same as the traditional hyphen, sometimes double encoded with
> the hyphen.
> 
> That being said, it is recommended to not include it in the font at all,
> because discretionary hyphenation should be handled at the level of the
> shaping engine, not the font. Also, even if present, the software would
> not display that character.
> 
> More discussion at:
> https://typedrawers.com/discussion/2046/special-dash-things-softhyphen-horizontalbar
> 




> Original proposal: https://github.com/fonttools/fontbakery/issues/4046
> See also: https://github.com/fonttools/fontbakery/issues/3486





* ⚠️ **WARN** <p>This font has a 'Soft Hyphen' character.</p>
 [code: softhyphen]



</div>
</details>
</div>
</details>

<details><summary>[3] Loligora-Italic[wght].ttf</summary>
<div>
<details>
    <summary>⚠️ <b>WARN</b> Ensure variable fonts include an avar table. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#mandatory-avar-table">mandatory_avar_table</a></summary>
    <div>


> 
> Most variable fonts should include an avar table to correctly define
> axes progression rates.
> 
> For example, a weight axis from 0% to 100% doesn't map directly to 100 to 1000,
> because a 10% progression from 0% may be too much to define the 200,
> while 90% may be too little to define the 900.
> 
> If the progression rates of axes is linear, this check can be ignored.
> Fontmake will also skip adding an avar table if the progression rates
> are linear. However, it is still recommended that designers visually proof
> each instance is at the expected weight, width etc.
> 




> Original proposal: https://github.com/fonttools/fontbakery/issues/3100





* ⚠️ **WARN** <p>This variable font does not have an avar table. Most variable fonts should include an avar table to correctly define axes progression rates.</p>
 [code: missing-avar]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check there are no overlapping path segments <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#overlapping-path-segments">overlapping_path_segments</a></summary>
    <div>


> 
> Some rasterizers encounter difficulties when rendering glyphs with
> overlapping path segments.
> 
> A path segment is a section of a path defined by two on-curve points.
> When two segments share the same coordinates, they are considered
> overlapping.
> 




> Original proposal: https://github.com/google/fonts/issues/7594#issuecomment-2401909084





* ⚠️ **WARN** <p>The following glyphs have overlapping path segments:</p>
<pre><code>* yen (U+00A5): L&lt;&lt;328.0,300.0&gt;--&lt;233.0,300.0&gt;&gt; has the same coordinates as a previous segment.

* four (U+0034): L&lt;&lt;441.0,720.0&gt;--&lt;525.0,720.0&gt;&gt; has the same coordinates as a previous segment.

* two.pnum: L&lt;&lt;409.0,403.0&gt;--&lt;467.0,346.0&gt;&gt; has the same coordinates as a previous segment.

* four.pnum: L&lt;&lt;445.0,720.0&gt;--&lt;529.0,720.0&gt;&gt; has the same coordinates as a previous segment.

* two (U+0032): L&lt;&lt;405.0,403.0&gt;--&lt;463.0,346.0&gt;&gt; has the same coordinates as a previous segment.

* g (U+0067): B&lt;&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;&gt; has the same coordinates as a previous segment.

* g (U+0067): B&lt;&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;&gt; has the same coordinates as a previous segment.

* g (U+0067): B&lt;&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;&gt; has the same coordinates as a previous segment.

* g (U+0067): B&lt;&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;&gt; has the same coordinates as a previous segment.

* g (U+0067): B&lt;&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;-&lt;281.0,-142.0&gt;&gt; has the same coordinates as a previous segment.

* 72 more.
</code></pre>
<p>Use -F or --full-lists to disable shortening of long lists.</p>
 [code: overlapping-path-segments]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Does the font contain a soft hyphen? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#soft-hyphen">soft_hyphen</a></summary>
    <div>


> 
> The 'Soft Hyphen' character (codepoint 0x00AD) is used to mark
> a hyphenation possibility within a word in the absence of or
> overriding dictionary hyphenation.
> 
> It is sometimes designed empty with no width (such as a control character),
> sometimes the same as the traditional hyphen, sometimes double encoded with
> the hyphen.
> 
> That being said, it is recommended to not include it in the font at all,
> because discretionary hyphenation should be handled at the level of the
> shaping engine, not the font. Also, even if present, the software would
> not display that character.
> 
> More discussion at:
> https://typedrawers.com/discussion/2046/special-dash-things-softhyphen-horizontalbar
> 




> Original proposal: https://github.com/fonttools/fontbakery/issues/4046
> See also: https://github.com/fonttools/fontbakery/issues/3486





* ⚠️ **WARN** <p>This font has a 'Soft Hyphen' character.</p>
 [code: softhyphen]



</div>
</details>
</div>
</details>




### Summary

| 💥 ERROR | ☠ FATAL | 🔥 FAIL | ⚠️ WARN | ⏩ SKIP | ℹ️ INFO | ✅ PASS | 🔎 DEBUG | 
| ---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 6 | 41 | 6 | 189 | 0 | 
| 0% | 0% | 0% | 2% | 17% | 2% | 78% | 0% | 



**Note:** The following loglevels were omitted in this report:


* SKIP
* INFO
* PASS
* DEBUG
