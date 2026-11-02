# Physical implementation status

This is an unfinished physical implementation, **not a manufacturable calculator**.

| Item | Status |
| --- | --- |
| Calculator RTL, unsigned 8-bit A/B | Implemented |
| All 262,144 arithmetic input combinations | Passed synthesized generic-gate simulation |
| Reset and enable-pause | Passed |
| SKY130 standard-cell mapping and coordinate worksheet | Implemented, 469 cells |
| Full calculator GDS | Real cell geometry, placement only |
| Initial coordinate worksheet | Script-seeded rows, not individually hand-optimized |
| Hand-specified full-adder cell positions and tracks | Experimental standalone block |
| Full-calculator manual interconnect | Missing |
| Supply/bulk taps, fillers, antenna repair, clock network | Missing |
| DRC / extracted LVS / parasitic timing | Not run |
| Current official SKY130 tile dimensions | Checked at pinned tt-support-tools commit |
| Pin template and selected-shuttle PDK revision | Must be revalidated |
| Mathematically smallest area | Not established |

The hand-routed full-adder does NOT replace the adder in the synthesized calculator.
The generic-to-SKY130 cell map is a direct logical mapping, not timing-driven technology mapping.
The exhaustive test is on generic synthesized gates, not extracted layout or SKY130 transistor models.

The layout checkpoint uses a 161.00 x 111.52 um target rectangle from
`TinyTapeout/tt-support-tools/tech/sky130A/tile_sizes.yaml`, commit
`b7b993ac507a3d0dd9c2c82c213ff6fab7d6dacc`. Its 4,446.765 um²
cell area is 24.77% of that rectangle. This ratio excludes routing, clock, power,
well/tap/filler cells and therefore does not prove that a complete design fits.

Remaining work, in dependency order:

1. Confirm SKY26d uses this boundary, then obtain its pin shapes and PDK revision.
2. Review and hand-adjust `layout/placement.csv` for clock/power/routing access.
3. Specify and implement every net, including supply and bulk connections.
4. Add taps, fillers, clock buffering and necessary antenna protection.
5. Run the official SKY130 DRC deck and extracted LVS against the mapped netlist.
6. Run parasitic timing and gate-level tests, then Tiny Tapeout precheck.
7. Review manufacturing options and delivery separately before purchasing.

The official `.github/workflows/gds.yaml` creates an **automatic reference layout**.
It is not evidence that the manual layout passed or that the two layouts match.
