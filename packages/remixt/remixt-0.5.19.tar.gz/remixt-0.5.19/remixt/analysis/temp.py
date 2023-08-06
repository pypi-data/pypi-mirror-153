import remixt.utils
import remixt.seqdataio
import numpy as np
import fire


def calculate_fragment_stats(genome_fasta, seqdata_filename):
    """
    """
    data = []

    for chrom_id, chrom_sequence in remixt.utils.read_sequences(genome_fasta):
        chrom_sequence = np.array(list(chrom_sequence.upper()), dtype=np.character)
        gc_indicator = ((chrom_sequence == b'G') | (chrom_sequence == b'C')) * 1
        gc_cumsum = gc_indicator.cumsum()

        reads_iter = remixt.seqdataio.read_fragment_data(
            seqdata_filename, chrom_id,
            filter_duplicates=True,
            map_qual_threshold=10,
            chunksize=1000000)

        for chrom_reads in reads_iter:
            chrom_reads['gc_sum'] = gc_cumsum[chrom_reads['end'].values] - gc_cumsum[chrom_reads['start'].values]
            chrom_reads['fragment_length'] = chrom_reads['end'].values - chrom_reads['start'].values

            data.append(chrom_reads.groupby(['gc_sum', 'fragment_length']).size().rename('count').reset_index())

    data = pd.concat(data, ignore_index=True)
    data = data.groupby(['gc_sum', 'fragment_length']).sum().reset_index()


if __name__ == '__main__':
    fire.Fire(calculate_fragment_stats)

