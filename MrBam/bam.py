from MrBam.tools import memo, try_append

def get_reads(o, sam, chr, pos):
    "get all reads covers chr:pos"

    pos = int(pos) - 1 # 0-based leftmost coordinate

    for read in sam.fetch(chr, pos, pos+1):
        aligned_pairs = read.get_aligned_pairs(matches_only=True)

        try:
            query_pos = next(qpos for qpos, rpos in aligned_pairs if rpos == pos)
        except:
            continue

        yield (
            read.query_name,
            read.query_sequence[query_pos],
            read.query_qualities[query_pos],
            read.reference_start - read.query_alignment_start,
            read.infer_query_length(),
            read.next_reference_start,
            abs(read.template_length),
            read.is_reverse,
            read.is_paired and not read.mate_is_unmapped
        )

@memo
def pad_softclip(sam):
    "return a dict of name -> startpos, length, where softclipped basees were padded"

    namedict, pairdict = {}, {}

    for read in sam.fetch():
        if not read.is_paired or read.mate_is_unmapped:
            continue

        adjusted_start = read.reference_start - read.query_alignment_start
        adjusted_end   = adjusted_start + read.infer_query_length()
        name           = read.query_name

        try_append(namedict, name, (adjusted_start, adjusted_end))

    for k, v in namedict.items():
        if len(v) != 2:
            pass #TODO
        else:
            start  = min(map(lambda x: x[0], v))
            length = max(map(lambda x: x[1], v)) - start
            pairdict[k] = start, length

    return pairdict
