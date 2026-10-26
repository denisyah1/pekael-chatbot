-- Pandoc Lua filter for Pekael Word exports (scripts/export_docs.py).
-- * the first level-1 heading is removed (the title is printed in the page header)
-- * level-2 headings become numbered Heading 1 ("1. Tujuan"), deeper levels shift up by one
-- * links keep only their text, inline code becomes plain text
-- * <br> inside table cells becomes a line break, lines inside block quotes stay separate
-- * tables with an empty header row lose that row (they are label/value tables)
-- * checkbox options written on separate lines stay on separate lines

local title_removed = false
local section = 0

function Header(el)
  if el.level == 1 and not title_removed then
    title_removed = true
    return {}
  end
  if el.level == 2 then
    section = section + 1
    el.content:insert(1, pandoc.Space())
    el.content:insert(1, pandoc.Str(section .. "."))
  end
  el.level = math.max(1, el.level - 1)
  return el
end

function Link(el)
  return el.content
end

function Code(el)
  return pandoc.Str(el.text)
end

function RawInline(el)
  if el.format == "html" and el.text:match("^<br%s*/?>$") then
    return pandoc.LineBreak()
  end
end

-- Label/value tables are written with an empty header row ("| | |") in Markdown: drop it.
function Table(tbl)
  for _, row in ipairs(tbl.head.rows) do
    for _, cell in ipairs(row.cells) do
      if #cell.contents > 0 then
        return nil
      end
    end
  end
  tbl.head = pandoc.TableHead()
  return tbl
end

local function keep_lines(el)
  return pandoc.walk_block(el, { SoftBreak = function() return pandoc.LineBreak() end })
end

function BlockQuote(el)
  return keep_lines(el)
end

-- Checkbox options ("☐ Ya" on separate source lines) stay on separate lines.
function Para(el)
  if pandoc.utils.stringify(el):find("☐", 1, true) then
    return pandoc.Div({ keep_lines(el) }, { ["custom-style"] = "Checklist" })
  end
end
