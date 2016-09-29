from MrBam.tools import try_append

def aggregate_reads(o, reads, adjusted_pos=None):
    "aggregate reads by startpos, endpos and base"

    name_dict     = {} # name -> reads
    unique_pairs  = {} # start, length, is_overlap -> [base, quality]
    unique_single = {} # start, length, is_reverse -> [base, quality]

    nsum,  nerror    = 0, 0 # depth, errors (such as 3 reads share the same name)
    nlowq, ninconsis = 0, 0 # low quality bases, inconsistent pairs (count on reads)

    for read in reads:
        name, *info = read
        try_append(name_dict, name, info)
        nsum += 1

    for name, reads in name_dict.items():
        if len(reads) == 1: # non-overlap or single
            base, qual, r1start, r1len, r2start, tlen, isrev, paired = reads[0]

            if qual <= o.qual:
                nlowq += 1
                continue

            if paired:
                if o.fast:
                    start = min(r1start, r2start)
                else:
                    start, tlen = adjusted_pos[name]
                try_append(unique_pairs, (start, tlen, False), (base, qual))
            else:
                try_append(unique_single, (r1start, r1len, isrev), (base, qual))

        elif len(reads) == 2: # overlap
            r1, r2 = reads
            r1base, r1qual, r1start, r1len, *_ = r1
            r2base, r2qual, r2start, r2len, *_ = r2

            if r1qual <= o.qual or r2qual <= o.qual:
                nlowq += 2
                continue

            if r1base != r2base:
                ninconsis += 2
                continue

            start = min(r1start, r2start)
            tlen  = max(r1start+r1len, r2start+r2len) - start
            qual  = max(r1qual, r2qual)

            try_append(unique_pairs, (start, tlen, True), (r1base, qual))

        else: # error
            if o.verbos:
                print("%s: more than 2 reads (%d total) share the same name; all droped." % (name, len(reads)))
            nerror += len(reads)

    return unique_pairs, unique_single, nsum, nerror, nlowq, ninconsis
