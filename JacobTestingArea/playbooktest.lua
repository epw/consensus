local function pagereflink(format, link)
  if format:match 'latex' then
    return pandoc.RawInline('latex', '(page \\pageref{' .. link .. '})')
  elseif format:match 'html.*' then
    return pandoc.RawInline('html', '<a href=#' .. link .. '>here</a>')
  else
    -- fall back to insert a form feed character
    return pandoc.Str("Whoops")
  end
end

local function pagerefanchor(format, anchor)
  if format:match 'latex' then
    return pandoc.RawInline('latex', '\\label{' .. anchor .. '}')
  elseif format:match 'html.*' then
    return pandoc.RawInline('html', '<a id="' .. anchor .. '"></a>')
  else
    -- fall back to insert a form feed character
    return pandoc.Str("Whoops")
  end
end

return {
  {
  Str = function (elem)
    if elem.text:match "{{start.*}}" then
		playbook = (elem.text:match "{{start(.*)}}")
		return pagereflink(FORMAT, link)
	elseif elem.text:match "{{end.*}}" then
	  anchor = (elem.text:match "{{anchor(.*)}}")
	  return pagerefanchor(FORMAT, anchor)
    else
      return elem
    end
  end,
  }
}