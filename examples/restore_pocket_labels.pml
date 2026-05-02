# Example: restore residue labels for pocket (protein within 3 Å of ligand).
# In PyMOL: File → Run Script, or: @examples/restore_pocket_labels.pml

python
from pymol import cmd

cmd.select("pocket5", "byres (polymer.protein within 3 of organic)")
cmd.delete("lb_*")

m = cmd.get_model("pocket5 and name CA")
seen = set()
idx = 0
for at in m.atom:
    key = (at.chain, at.resn, at.resi)
    if key in seen:
        continue
    seen.add(key)
    x, y, z = at.coord
    ch, rn, ri = at.chain, at.resn, str(at.resi).strip()
    nm = "lb_%d" % idx
    idx += 1
    cmd.pseudoatom(nm, pos=[x, y + 8.0, z], label="%s %s %s" % (ch, rn, ri))

cmd.show("labels", "lb_*")
cmd.set("label_size", 22, "lb_*")
cmd.set("label_color", "tv_yellow", "lb_*")
cmd.set("label_outline_color", "black", "lb_*")

cmd.label("all", "")
cmd.label("organic", "")
cmd.label("pocket5 and name CA", "'%s %s' % (resn,resi)")
cmd.set("label_size", 18, "pocket5 and name CA")
cmd.set("label_color", "yellow", "pocket5 and name CA")
cmd.set("depth_cue", 0)
python end
