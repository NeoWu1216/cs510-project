
import sys
import metapy
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python {} n_topics".format(sys.argv[0]))
        sys.exit(1)
    else:
        _num_topics = int(sys.argv[1])

    _output_prefix = "output"
    metapy.log_to_stderr()
    fidx = metapy.index.make_forward_index('config.toml')
    dset = metapy.learn.Dataset(fidx)


    lda_inf = metapy.topics.LDAGibbs(dset, num_topics=_num_topics, alpha=0.1, beta=0.1)
    lda_inf.run(num_iters=500)
    lda_inf.save(_output_prefix)

    model = metapy.topics.TopicModel(_output_prefix)

    with open(_output_prefix+'-topic.txt','w+') as topic:
        for topic_id in range(_num_topics):
            print('Topic ' + str(topic_id))
            print([(fidx.term_text(pr[0]), pr[1]) for pr in model.top_k(tid=topic_id, k = 20)])
            topic.write('Topic ' + str(topic_id) + '\n')
            topic.write(str([(fidx.term_text(pr[0]), pr[1]) for pr in model.top_k(tid=topic_id, k = 20)]))
            topic.write('\n')

    target_doc_count = 5
    with open(_output_prefix+'-document.txt','w+') as doc:
        for d_id in range(target_doc_count):
            print('Document ' + str(d_id))
            print(model.topic_distribution(d_id))
            doc.write('Document ' + str(d_id) + '\n')
            doc.write(str(model.topic_distribution(d_id)))
            doc.write('\n')